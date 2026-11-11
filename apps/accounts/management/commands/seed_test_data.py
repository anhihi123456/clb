from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson, Enrollment

User = get_user_model()


class Command(BaseCommand):
    help = "Khởi tạo dữ liệu mẫu cho kiểm thử phân quyền và thiết lập khóa học"

    def handle(self, *args, **options):
        self.stdout.write("Bắt đầu khởi tạo dữ liệu mẫu...")

        # 1. Tạo tài khoản Admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@o365.edu.vn',
                'first_name': 'Ban',
                'last_name': 'Quản Trị',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS("Đã tạo Admin: admin / admin123"))

        # 2. Tạo tài khoản Giảng viên
        teacher1, created = User.objects.get_or_create(
            username='teacher_word',
            defaults={
                'email': 'teacher.word@o365.edu.vn',
                'first_name': 'Nguyễn Văn',
                'last_name': 'Giảng Viên Word',
                'role': 'teacher',
                'is_staff': True,
            }
        )
        if created:
            teacher1.set_password('teacher123')
            teacher1.save()
            self.stdout.write(self.style.SUCCESS("Đã tạo Giảng viên: teacher_word / teacher123"))

        teacher2, created = User.objects.get_or_create(
            username='teacher_excel',
            defaults={
                'email': 'teacher.excel@o365.edu.vn',
                'first_name': 'Trần Thị',
                'last_name': 'Giảng Viên Excel',
                'role': 'teacher',
                'is_staff': True,
            }
        )
        if created:
            teacher2.set_password('teacher123')
            teacher2.save()
            self.stdout.write(self.style.SUCCESS("Đã tạo Giảng viên: teacher_excel / teacher123"))

        # 3. Tạo tài khoản Học viên mẫu
        student1, created = User.objects.get_or_create(
            username='sv001',
            defaults={
                'email': 'student1@sis.edu.vn',
                'first_name': 'Lê Văn',
                'last_name': 'An',
                'student_id': '20210001',
                'class_name': 'CNTT-01',
                'role': 'student',
            }
        )
        if created:
            student1.set_password('sv123')
            student1.save()
            self.stdout.write(self.style.SUCCESS("Đã tạo Học viên: sv001 (MSSV: 20210001) / sv123"))

        student2, created = User.objects.get_or_create(
            username='sv002',
            defaults={
                'email': 'student2@sis.edu.vn',
                'first_name': 'Phạm Thị',
                'last_name': 'Bình',
                'student_id': '20210002',
                'class_name': 'CNTT-02',
                'role': 'student',
            }
        )
        if created:
            student2.set_password('sv123')
            student2.save()
            self.stdout.write(self.style.SUCCESS("Đã tạo Học viên: sv002 (MSSV: 20210002) / sv123"))

        # 4. Khởi tạo 3 Khóa học cốt lõi
        course_word, _ = Course.objects.get_or_create(
            code='WORD',
            defaults={
                'title': 'Kỹ năng soạn thảo văn bản chuẩn với Microsoft Word',
                'description': 'Khóa học hướng dẫn soạn thảo công văn, đồ án tốt nghiệp, mục lục tự động và định dạng chuẩn học thuật.',
            }
        )
        course_word.instructors.add(teacher1)

        course_excel, _ = Course.objects.get_or_create(
            code='EXCEL',
            defaults={
                'title': 'Xử lý dữ liệu & Lập báo cáo chuyên nghiệp với Microsoft Excel',
                'description': 'Làm chủ các hàm tìm kiếm, xử lý chuỗi, PivotTable và xây dựng Dashboard phân tích số liệu.',
            }
        )
        course_excel.instructors.add(teacher2)

        course_ppt, _ = Course.objects.get_or_create(
            code='PPT',
            defaults={
                'title': 'Thiết kế bài thuyết trình ấn tượng với Microsoft PowerPoint',
                'description': 'Nguyên lý phối màu, typography, bố cục trực quan và kỹ thuật tạo chuyển động mượt mà.',
            }
        )
        course_ppt.instructors.add(teacher1, teacher2)

        # 5. Khởi tạo bài học mẫu có nhúng YouTube và Google Drive
        # Bài học cho Word
        Lesson.objects.get_or_create(
            course=course_word,
            order=1,
            defaults={
                'title': 'Bài 1: Tổng quan giao diện và kỹ thuật thụt lề chuẩn quy chuẩn',
                'lesson_type': 'video',
                'raw_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'content_text': 'Xem kỹ video hướng dẫn cách căn chỉnh lề (Margins) 2-2-3-2 theo quy định chuẩn văn bản hành chính Việt Nam.',
                'duration_seconds': 360,
                'min_watch_percent': 80,
                'is_published': True,
            }
        )

        Lesson.objects.get_or_create(
            course=course_word,
            order=2,
            defaults={
                'title': 'Bài 2: Tài liệu thực hành định dạng văn bản chuẩn (PDF)',
                'lesson_type': 'document',
                'raw_url': 'https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view',
                'content_text': 'Tải hoặc đọc trực tiếp tài liệu đề bài thực hành số 1 bên dưới.',
                'is_published': True,
            }
        )

        # Bài học cho Excel
        Lesson.objects.get_or_create(
            course=course_excel,
            order=1,
            defaults={
                'title': 'Bài 1: Làm chủ hàm VLOOKUP, XLOOKUP và INDEX-MATCH',
                'lesson_type': 'video',
                'raw_url': 'https://youtu.be/dQw4w9WgXcQ',
                'content_text': 'Phân biệt ưu nhược điểm của VLOOKUP truyền thống và XLOOKUP trong Office 365.',
                'duration_seconds': 480,
                'min_watch_percent': 85,
                'is_published': True,
            }
        )

        # 6. Ghi danh sinh viên vào khóa học
        for c in [course_word, course_excel, course_ppt]:
            Enrollment.objects.get_or_create(user=student1, course=c)
            Enrollment.objects.get_or_create(user=student2, course=c)

        self.stdout.write(self.style.SUCCESS("Khởi tạo dữ liệu mẫu thành công!"))

