from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def teacher_required(view_func):
    """Bắt buộc người dùng đăng nhập và có vai trò Giảng viên hoặc Quản trị viên"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_teacher_or_admin:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Bạn không có quyền truy cập khu vực dành cho Giảng viên.")
        return redirect('courses:course_list')
    return _wrapped_view


def admin_required(view_func):
    """Bắt buộc người dùng có vai trò Quản trị viên / Ban tổ chức"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'admin' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Bạn không có quyền truy cập khu vực Quản trị.")
        return redirect('courses:course_list')
    return _wrapped_view

