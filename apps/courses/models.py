from django.db import models
from django.conf import settings
from .embed_utils import parse_media_url, EmbedParseError


class Course(models.Model):
    CODE_CHOICES = (
        ('WORD', 'Microsoft Word'),
        ('EXCEL', 'Microsoft Excel'),
        ('PPT', 'Microsoft PowerPoint'),
    )
    code = models.CharField(
        max_length=10,
        choices=CODE_CHOICES,
        unique=True,
        verbose_name="Mã khóa học"
    )
    title = models.CharField(max_length=200, verbose_name="Tên khóa học")
    description = models.TextField(blank=True, verbose_name="Mô tả khóa học")
    instructors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teaching_courses',
        blank=True,
        verbose_name="Giảng viên phụ trách"
    )
    is_active = models.BooleanField(default=True, verbose_name="Đang mở")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Khóa học"
        verbose_name_plural = "Khóa học"
        ordering = ['code']

    def __str__(self):
        return f"[{self.code}] {self.title}"

    @property
    def total_lessons(self):
        return self.lessons.count()

    @property
    def published_lessons(self):
        return self.lessons.filter(is_published=True).order_by('order')


class Lesson(models.Model):
    TYPE_CHOICES = (
        ('video', 'Video bài giảng (YouTube)'),
        ('document', 'Tài liệu / Slide (Google Drive PDF/Slide)'),
        ('quiz', 'Bài kiểm tra (Google Forms)'),
        ('text', 'Nội dung bài đọc / Hướng dẫn'),
    )

    PROVIDER_CHOICES = (
        ('youtube', 'YouTube'),
        ('gdrive', 'Google Drive (PDF/File)'),
        ('gslides', 'Google Slides'),
        ('gdocs', 'Google Docs'),
        ('gforms', 'Google Forms'),
        ('none', 'Nội bộ'),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Khóa học"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề bài học")
    order = models.PositiveIntegerField(default=1, verbose_name="Thứ tự hiển thị")
    lesson_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='video',
        verbose_name="Loại học liệu"
    )
    raw_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Đường dẫn liên kết",
        help_text="Dán link YouTube thường, link chia sẻ Google Drive (PDF/Slide) hoặc link Google Forms"
    )
    embed_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Đường dẫn nhúng an toàn"
    )
    external_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Mã định danh bên thứ ba"
    )
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default='none',
        verbose_name="Nhà cung cấp"
    )
    content_text = models.TextField(
        blank=True,
        verbose_name="Nội dung ghi chú / Hướng dẫn"
    )
    duration_seconds = models.PositiveIntegerField(
        default=0,
        verbose_name="Thời lượng video (giây)",
        help_text="Nhập thời lượng video (nếu biết) để hệ thống tính % chính xác"
    )
    min_watch_percent = models.PositiveIntegerField(
        default=80,
        verbose_name="Ngưỡng đạt (% xem)",
        help_text="Giảng viên quy định % tối thiểu để tính là hoàn thành bài"
    )
    is_published = models.BooleanField(default=True, verbose_name="Đã xuất bản (Công khai)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bài học"
        verbose_name_plural = "Bài học"
        ordering = ['course', 'order', 'id']

    def __str__(self):
        return f"{self.course.code} - Bài {self.order}: {self.title}"

    def save(self, *args, **kwargs):
        # Auto parse embed URL when raw_url is provided
        if self.raw_url and self.raw_url.strip():
            try:
                info = parse_media_url(self.raw_url, expected_type=self.lesson_type)
                self.embed_url = info['embed_url']
                self.external_id = info['external_id']
                self.provider = info['provider']
            except EmbedParseError:
                # If cannot parse and not text, leave embed_url empty
                pass
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Học viên"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Khóa học"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ghi danh"
        verbose_name_plural = "Ghi danh"
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} -> {self.course.code}"
