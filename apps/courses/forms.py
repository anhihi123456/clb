from django import forms
from .models import Course, Lesson
from .embed_utils import parse_media_url, EmbedParseError


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'placeholder': 'Nhập tên khóa học'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'rows': 4,
                'placeholder': 'Mô tả tóm tắt mục tiêu khóa học...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title', 'order', 'lesson_type', 'raw_url',
            'content_text', 'duration_seconds', 'min_watch_percent', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'placeholder': 'Ví dụ: Bài 1: Kỹ thuật căn chỉnh lề chuẩn văn bản'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'min': 1
            }),
            'lesson_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none bg-white',
                'id': 'id_lesson_type'
            }),
            'raw_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none font-mono text-sm',
                'placeholder': 'Dán link YouTube (https://youtu.be/...) hoặc link Google Drive (https://drive.google.com/file/d/.../view)',
                'id': 'id_raw_url'
            }),
            'content_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'rows': 4,
                'placeholder': 'Ghi chú, yêu cầu bài tập hoặc lưu ý của giảng viên dành cho học viên...'
            }),
            'duration_seconds': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'placeholder': 'Thời lượng video (giây) - ví dụ 600 = 10 phút'
            }),
            'min_watch_percent': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'min': 0,
                'max': 100
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        lesson_type = cleaned_data.get('lesson_type')
        raw_url = cleaned_data.get('raw_url', '')

        if lesson_type in ('video', 'document', 'quiz'):
            if not raw_url or not raw_url.strip():
                self.add_error('raw_url', 'Vui lòng dán liên kết cho loại bài học này.')
            else:
                try:
                    info = parse_media_url(raw_url, expected_type=lesson_type)
                    # Gán sẵn vào instance
                    self.instance.embed_url = info['embed_url']
                    self.instance.external_id = info['external_id']
                    self.instance.provider = info['provider']
                except EmbedParseError as e:
                    self.add_error('raw_url', str(e))

        return cleaned_data

