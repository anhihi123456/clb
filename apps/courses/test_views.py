from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson

User = get_user_model()


class TeacherCourseSetupTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Teacher, Student and Admin
        self.teacher = User.objects.create_user(
            username='teacher_test',
            password='password123',
            role='teacher',
            is_staff=True
        )
        self.student = User.objects.create_user(
            username='student_test',
            password='password123',
            student_id='20219999',
            role='student'
        )

        # Create Course
        self.course = Course.objects.create(
            code='WORD',
            title='Kỹ năng Microsoft Word',
            description='Mô tả khóa học Word'
        )
        self.course.instructors.add(self.teacher)

    def test_student_cannot_access_teacher_dashboard(self):
        self.client.login(username='student_test', password='password123')
        response = self.client.get(reverse('courses:teacher_dashboard'))
        # Should redirect student away with message
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('courses:course_list'))

    def test_teacher_can_access_teacher_dashboard(self):
        self.client.login(username='teacher_test', password='password123')
        response = self.client.get(reverse('courses:teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thiết lập Khóa học & Học liệu')
        self.assertContains(response, 'WORD')

    def test_teacher_can_create_lesson_with_youtube_embed(self):
        self.client.login(username='teacher_test', password='password123')
        create_url = reverse('courses:teacher_lesson_create', kwargs={'course_code': 'WORD'})
        
        post_data = {
            'title': 'Bài 1: Căn lề văn bản',
            'order': 1,
            'lesson_type': 'video',
            'raw_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'content_text': 'Hướng dẫn chi tiết căn lề 2-2-3-2',
            'duration_seconds': 300,
            'min_watch_percent': 80,
            'is_published': True,
        }
        response = self.client.post(create_url, post_data)
        self.assertEqual(response.status_code, 302)

        # Verify lesson was saved with auto-extracted embed info
        lesson = Lesson.objects.get(course=self.course, order=1)
        self.assertEqual(lesson.title, 'Bài 1: Căn lề văn bản')
        self.assertEqual(lesson.provider, 'youtube')
        self.assertEqual(lesson.external_id, 'dQw4w9WgXcQ')
        self.assertIn('https://www.youtube.com/embed/dQw4w9WgXcQ', lesson.embed_url)

    def test_teacher_can_create_lesson_with_gdrive_embed(self):
        self.client.login(username='teacher_test', password='password123')
        create_url = reverse('courses:teacher_lesson_create', kwargs={'course_code': 'WORD'})
        
        post_data = {
            'title': 'Bài 2: Tài liệu PDF thực hành',
            'order': 2,
            'lesson_type': 'document',
            'raw_url': 'https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing',
            'content_text': 'Đọc file PDF đính kèm',
            'duration_seconds': 0,
            'min_watch_percent': 80,
            'is_published': True,
        }
        response = self.client.post(create_url, post_data)
        self.assertEqual(response.status_code, 302)

        lesson = Lesson.objects.get(course=self.course, order=2)
        self.assertEqual(lesson.provider, 'gdrive')
        self.assertEqual(lesson.external_id, '1A2B3C4D5E6F7G8H9I0J')
        self.assertEqual(lesson.embed_url, 'https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/preview')

    def test_api_parse_embed_preview(self):
        api_url = reverse('courses:api_parse_embed')
        response = self.client.get(api_url, {'url': 'https://youtu.be/dQw4w9WgXcQ', 'type': 'video'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['valid'])
        self.assertEqual(data['provider'], 'youtube')
        self.assertEqual(data['external_id'], 'dQw4w9WgXcQ')

    def test_student_can_view_lesson_embed(self):
        # Create a lesson
        lesson = Lesson.objects.create(
            course=self.course,
            title='Bài học xem video',
            order=1,
            lesson_type='video',
            raw_url='https://youtu.be/dQw4w9WgXcQ',
            is_published=True
        )

        detail_url = reverse('courses:lesson_detail', kwargs={'course_code': 'WORD', 'order': 1})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iframe')
        self.assertContains(response, 'https://www.youtube.com/embed/dQw4w9WgXcQ')
