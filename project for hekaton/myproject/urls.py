from django.urls import path
from .views import mark_attendance_face, mark_attendance_qr

app_name = "attendance"

urlpatterns = [
    path('api/mark/face/', mark_attendance_face, name='mark_attendance_face'),
    path('api/mark/qr/', mark_attendance_qr, name='mark_attendance_qr'),
]


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('attendance/', include('attendance.urls', namespace='attendance')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
