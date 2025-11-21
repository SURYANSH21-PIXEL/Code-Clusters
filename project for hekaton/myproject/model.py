from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='student_photos/')  # reference photo
    qr_token = models.CharField(max_length=128, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.roll_no} - {self.user.get_full_name() or self.user.username}"


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extra fields if needed

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Attendance(models.Model):
    MARKED_BY_CHOICES = (
        ('face', 'Face'),
        ('qr', 'QR'),
    )
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=True)
    marked_by = models.CharField(max_length=20, choices=MARKED_BY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.roll_no} - {self.date} - {self.status}"
