from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'student_id', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'student_id', 'first_name', 'last_name', 'email')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Thông tin sinh viên & vai trò LMS', {
            'fields': ('role', 'student_id', 'class_name', 'phone')
        }),
    )
