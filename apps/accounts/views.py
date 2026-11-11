from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên đăng nhập / Email",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
            'placeholder': 'admin, teacher_word, hoặc sv001'
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
            'placeholder': '••••••••'
        })
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('courses:course_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Đăng nhập thành công! Xin chào {user.get_full_name() or user.username}.")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                if user.is_teacher_or_admin:
                    return redirect('courses:teacher_dashboard')
                return redirect('courses:course_list')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác.")
    else:
        form = LoginForm()

    # Lấy danh sách tài khoản mẫu để hiển thị nút đăng nhập nhanh (Quick Test)
    test_accounts = [
        {'role': 'Giảng viên Word', 'username': 'teacher_word', 'desc': 'Quản lý khóa Word'},
        {'role': 'Giảng viên Excel', 'username': 'teacher_excel', 'desc': 'Quản lý khóa Excel'},
        {'role': 'Học viên', 'username': 'sv001', 'desc': 'MSSV: 20210001'},
        {'role': 'Ban tổ chức (Admin)', 'username': 'admin', 'desc': 'Toàn quyền hệ thống'},
    ]

    return render(request, 'accounts/login.html', {
        'form': form,
        'test_accounts': test_accounts,
    })


def logout_view(request):
    logout(request)
    messages.info(request, "Bạn đã đăng xuất khỏi hệ thống.")
    return redirect('courses:course_list')


def quick_switch_user(request, username):
    """Tính năng hỗ trợ DEV/Testing: Đăng nhập nhanh 1-chạm không cần gõ mật khẩu"""
    target_user = User.objects.filter(username=username).first()
    if target_user:
        login(request, target_user)
        messages.success(request, f"Đã chuyển sang vai trò: [{target_user.get_role_display()}] {target_user.get_full_name() or target_user.username}")
        if target_user.is_teacher_or_admin:
            return redirect('courses:teacher_dashboard')
        return redirect('courses:course_list')
    else:
        messages.error(request, f"Không tìm thấy tài khoản {username}. Hãy chạy `python manage.py seed_test_data` trước.")
        return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })
