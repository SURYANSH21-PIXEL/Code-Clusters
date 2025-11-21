from datetime import date

import face_recognition
import numpy as np
from django.utils import timezone
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Student, Attendance
from .utils_face import load_known_encodings

# simple in-memory cache (improve for production)
KNOWN = None


def get_known():
    global KNOWN
    if KNOWN is None:
        KNOWN = load_known_encodings()
    return KNOWN


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def mark_attendance_face(request):
    """
    Receive file field 'image' (jpg/png) — a photo from webcam.
    Return matched student or error.
    """
    file = request.FILES.get('image')
    if not file:
        return Response({"ok": False, "error": "No image provided"}, status=400)

    try:
        img = face_recognition.load_image_file(file)
    except Exception as e:
        return Response({"ok": False, "error": f"Invalid image: {e}"}, status=400)

    encs = face_recognition.face_encodings(img)
    if not encs:
        return Response({"ok": False, "error": "No face detected"}, status=400)

    unknown = encs[0]
    known = get_known()
    distances = []
    for sid, kenc in known:
        dist = np.linalg.norm(kenc - unknown)
        distances.append((sid, float(dist)))

    if not distances:
        return Response({"ok": False, "error": "No students enrolled"}, status=400)

    # find best match
    best = min(distances, key=lambda x: x[1])
    student_id, best_dist = best
    THRESH = 0.55  # adjust as needed

    if best_dist > THRESH:
        return Response(
            {"ok": False, "error": "No good match", "distance": best_dist},
            status=404,
        )

    student = Student.objects.get(pk=student_id)
    today = date.today()

    att, created = Attendance.objects.get_or_create(
        student=student,
        date=today,
        defaults={'marked_by': 'face', 'status': 'present'}
    )

    if not created:
        return Response(
            {"ok": True, "message": "Already marked", "student": student.roll_no}
        )

    return Response(
        {"ok": True, "message": "Attendance marked", "student": student.roll_no}
    )


@api_view(['GET'])
def mark_attendance_qr(request):
    token = request.GET.get('token')
    if not token:
        return Response({"ok": False, "error": "No token"}, status=400)

    try:
        student = Student.objects.get(qr_token=token)
    except Student.DoesNotExist:
        return Response({"ok": False, "error": "Invalid token"}, status=404)

    today = date.today()

    att, created = Attendance.objects.get_or_create(
        student=student,
        date=today,
        defaults={'marked_by': 'qr', 'status': 'present'}
    )

    if not created:
        return Response({"ok": True, "message": "Already marked"})

    return Response(
        {"ok": True, "message": "Marked by QR", "student": student.roll_no}
    )
