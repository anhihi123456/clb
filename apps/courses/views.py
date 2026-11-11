from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.accounts.decorators import teacher_required
from .models import Course, Lesson, Enrollment
from .forms import LessonForm, CourseForm
from .embed_utils import parse_media_url, EmbedParseError


# ========================================================
# 1. GIAO DIỆN HỌC VIÊN & CHUNG (PUBLIC / STUDENT VIEWS)
# ========================================================

def course_list(request):
    """Trang chủ: Danh sách 3 khóa học chính (Word, Excel, PPT)"""
    courses = Course.objects.filter(is_active=True).prefetch_related('lessons', 'instructors')
    user_enrolled_course_ids = []
    if request.user.is_authenticated:
        user_enrolled_course_ids = Enrollment.objects.filter(
            user=request.user
        ).values_list('course_id', flat=True)

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'user_enrolled_course_ids': set(user_enrolled_course_ids),
    })


def course_detail(request, course_code):
    """Trang chi tiết đề cương một khóa học"""
    course = get_object_or_404(Course, code=course_code.upper())
    
    # Nếu là giảng viên hoặc admin, xem được cả bài chưa xuất bản
    if request.user.is_authenticated and request.user.is_teacher_or_admin:
        lessons = course.lessons.all().order_by('order')
    else:
        lessons = course.lessons.filter(is_published=True).order_by('order')

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    })


def lesson_detail(request, course_code, order):
    """Trang học viên xem nội dung bài học (nhúng video, PDF, Slide hoặc Google Forms)"""
    course = get_object_or_404(Course, code=course_code.upper())
    
    if request.user.is_authenticated and request.user.is_teacher_or_admin:
        lesson = get_object_or_404(Lesson, course=course, order=order)
        all_lessons = list(course.lessons.all().order_by('order'))
    else:
        lesson = get_object_or_404(Lesson, course=course, order=order, is_published=True)
        all_lessons = list(course.lessons.filter(is_published=True).order_by('order'))

    # Tìm bài trước và bài sau để điều hướng
    current_index = all_lessons.index(lesson) if lesson in all_lessons else 0
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    })


def enroll_course(request, course_code):
    """Đăng ký tham gia khóa học cho học viên đã đăng nhập"""
    if not request.user.is_authenticated:
        messages.warning(request, "Vui lòng đăng nhập để tham gia khóa học.")
        return redirect('accounts:login')

    course = get_object_or_404(Course, code=course_code.upper())
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, f"Bạn đã tham gia thành công khóa học {course.title}!")
    else:
        messages.info(request, f"Bạn đã ghi danh vào khóa học này trước đó.")

    return redirect('courses:course_detail', course_code=course.code)


# ========================================================
# 2. KHU VỰC GIẢNG VIÊN (TEACHER COURSE SETUP & EMBED VIEWS)
# ========================================================

@teacher_required
def teacher_dashboard(request):
    """Bảng điều khiển Giảng viên: Tổng quan các khóa học và bài giảng"""
    # Nếu là Admin xem được tất cả, nếu là Giảng viên xem khóa được phân công (hoặc tất cả để phối hợp)
    courses = Course.objects.all().prefetch_related('lessons', 'instructors')
    return render(request, 'courses/teacher/dashboard.html', {
        'courses': courses,
    })


@teacher_required
def teacher_lesson_list(request, course_code):
    """Danh sách quản lý bài học trong một khóa học cụ thể"""
    course = get_object_or_404(Course, code=course_code.upper())
    lessons = course.lessons.all().order_by('order')

    return render(request, 'courses/teacher/lesson_list.html', {
        'course': course,
        'lessons': lessons,
    })


@teacher_required
def teacher_lesson_create(request, course_code):
    """Giảng viên thêm bài học mới với link nhúng YouTube / Drive / Google Forms"""
    course = get_object_or_404(Course, code=course_code.upper())
    
    # Tính thứ tự tiếp theo mặc định
    next_order = course.lessons.count() + 1

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, f"Đã thêm bài học '{lesson.title}' thành công!")
            return redirect('courses:teacher_lesson_list', course_code=course.code)
    else:
        form = LessonForm(initial={'order': next_order, 'min_watch_percent': 80})

    return render(request, 'courses/teacher/lesson_form.html', {
        'form': form,
        'course': course,
        'is_edit': False,
    })


@teacher_required
def teacher_lesson_update(request, course_code, lesson_id):
    """Giảng viên cập nhật bài học hiện có"""
    course = get_object_or_404(Course, code=course_code.upper())
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật bài học '{lesson.title}' thành công!")
            return redirect('courses:teacher_lesson_list', course_code=course.code)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'courses/teacher/lesson_form.html', {
        'form': form,
        'course': course,
        'lesson': lesson,
        'is_edit': True,
    })


@teacher_required
def teacher_lesson_delete(request, course_code, lesson_id):
    """Xóa bài học"""
    course = get_object_or_404(Course, code=course_code.upper())
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.method == 'POST':
        title = lesson.title
        lesson.delete()
        messages.success(request, f"Đã xóa bài học '{title}'!")
        return redirect('courses:teacher_lesson_list', course_code=course.code)

    return render(request, 'courses/teacher/lesson_confirm_delete.html', {
        'course': course,
        'lesson': lesson,
    })


@require_GET
def api_parse_embed_preview(request):
    """
    API JSON kiểm tra và sinh URL nhúng xem trước ngay khi Giảng viên gõ/dán link trên Form
    Endpoint: /courses/api/parse-embed/?url=...&type=...
    """
    url = request.GET.get('url', '').strip()
    expected_type = request.GET.get('type', '')

    if not url:
        return JsonResponse({'valid': False, 'error': 'Vui lòng nhập đường dẫn liên kết'})

    try:
        info = parse_media_url(url, expected_type=expected_type or None)
        return JsonResponse({
            'valid': True,
            'provider': info['provider'],
            'external_id': info['external_id'],
            'embed_url': info['embed_url'],
            'preview_url': info.get('preview_url', ''),
        })
    except EmbedParseError as e:
        return JsonResponse({'valid': False, 'error': str(e)})
