import uuid
from io import BytesIO

import face_recognition
import numpy as np
import qrcode
from django.core.files.base import ContentFile

from .models import Student


def load_known_encodings():
    """
    Load encodings for all students that have a photo.
    Returns list of tuples: (student_id, encoding_vector)
    """
    known_encodings = []
    students = Student.objects.all()
    for s in students:
        if not s.photo:
            continue
        img_path = s.photo.path
        print("Loading face photo:", img_path)  # for debug
        img = face_recognition.load_image_file(img_path)
        encs = face_recognition.face_encodings(img)
        if len(encs) > 0:
            known_encodings.append((s.id, encs[0]))
    return known_encodings


def generate_and_save_qr(student):
    """
    Generate a unique token and create a QR for the attendance URL.
    Returns a ContentFile of PNG image that you can save on a model ImageField.
    """
    token = student.qr_token
    if not token:
        token = str(uuid.uuid4())
        student.qr_token = token
        student.save(update_fields=['qr_token'])

    # IMPORTANT: change 'your-domain.com' to your real domain or localhost
    url = f"http://127.0.0.1:8000/attendance/api/mark/qr/?token={token}"

    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f'qr_{student.roll_no}.png')
