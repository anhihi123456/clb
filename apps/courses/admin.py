from django.contrib import admin
from .models import Course, Lesson, Enrollment


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('order', 'title', 'lesson_type', 'raw_url', 'is_published')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'is_active', 'total_lessons', 'created_at')
    list_filter = ('is_active', 'code')
    search_fields = ('code', 'title', 'description')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'order', 'title', 'lesson_type', 'provider', 'min_watch_percent', 'is_published')
    list_filter = ('course', 'lesson_type', 'provider', 'is_published')
    search_fields = ('title', 'content_text', 'external_id')
    ordering = ('course', 'order')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('user__username', 'user__student_id', 'course__title')
