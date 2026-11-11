from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Học viên'),
        ('teacher', 'Giảng viên'),
        ('admin', 'Quản trị viên / Ban tổ chức'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name="Vai trò"
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Mã sinh viên (MSSV)"
    )
    class_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Lớp sinh hoạt"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Số điện thoại"
    )

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def __str__(self):
        name = self.get_full_name() or self.username
        role_label = self.get_role_display()
        if self.student_id:
            return f"[{self.student_id}] {name} ({role_label})"
        return f"{name} ({role_label})"

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_teacher_or_admin(self):
        return self.role in ('teacher', 'admin') or self.is_staff or self.is_superuser
