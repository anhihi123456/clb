# KẾ HOẠCH TRIỂN KHAI PHẦN CORE HỆ THỐNG LMS (CLB o365)
**Vai trò:** Senior Web Developer / Tech Lead  
**Dự án:** o365_LMS - Hệ thống quản lý học tập phục vụ Khóa Kỹ Năng Mềm (Word, Excel, PowerPoint)  
**Quy mô:** ~300 sinh viên / khóa  
**Phiên bản:** 2.0 (Cập nhật theo phản hồi và quyết định kỹ thuật mới nhất)  
**Ngày cập nhật:** 10/11/2026  

---

## 1. TỔNG HỢP CÁC QUYẾT ĐỊNH KỸ THUẬT ĐÃ CHỐT

Dựa trên phản hồi thực tế từ đội ngũ tổ chức, kiến trúc phần CORE được chốt như sau:

1. **Xác thực & Định danh (Phương án B):**
   - Sử dụng **Google SSO** (`django-allauth`) cho môi trường thực tế.
   - **Form Onboarding bắt buộc:** Ngay sau lần đầu đăng nhập Google thành công, sinh viên bắt buộc phải khai báo **Mã sinh viên (MSSV)**, Họ và tên đầy đủ, Lớp sinh hoạt và Số điện thoại.
   - **Cơ chế Test Phân Quyền tiện lợi (Dev/Staging):** Cấu hình song song Django Built-in Authentication (Username/Password) và bộ dữ liệu mẫu (Fixtures/Seeder) tạo sẵn 3 tài khoản mẫu:
     - `admin` (Quản trị viên)
     - `teacher` (Giảng viên)
     - `student` (Học viên)  
     -> Giúp đội ngũ phát triển và kiểm thử dễ dàng chuyển đổi vai trò (switch role) ngay trên máy cục bộ mà không phụ thuộc vào Google Cloud Console hay mạng bên ngoài.
2. **Loại bỏ cơ chế Điểm danh Offline:**
   - Tạm thời gác lại toàn bộ module điểm danh (iCTSV / Dynamic QR) để tinh gọn hệ thống và tập trung nguồn lực phát triển phần lõi.
   - Công thức xét duyệt cấp minh chứng Kỹ năng mềm giai đoạn này:
     $$\text{Cấp Minh Chứng} = (\text{Tiến độ xem Video} \ge \text{Ngưỡng quy định}) \land (\text{Điểm Quiz Google Forms} \ge \text{Điểm sàn})$$
3. **Chuyển đổi Bài kiểm tra sang Google Forms:**
   - Thay thế Microsoft Forms bằng **Google Forms** để hợp nhất 100% hệ sinh thái Google (Google Auth, Google Drive, YouTube, Google Forms).
   - Nhúng Google Forms trực tiếp vào giao diện bài thi cuối khóa.
   - Thu thập điểm bằng cách: Giảng viên xuất bảng điểm từ Google Forms (Google Sheets / CSV) -> Tải file lên LMS -> Hệ thống tự động bóc tách và khớp điểm số theo **MSSV** hoặc **Google Email**.
4. **Cơ chế Video Player & Ngưỡng hoàn thành linh hoạt:**
   - **Ngưỡng đạt (% Completion):** Có thể tùy biến cấu hình bởi Giảng viên theo từng bài học (ví dụ: Bài A cần 80%, Bài B cần 90%, mặc định là 80%).
   - **Trải nghiệm phát video:** Cho phép học viên **tua lùi (seek backward)** thoải mái để nghe lại kiến thức chưa hiểu; **chặn tua vượt quá mốc thời gian cao nhất đã xem (furthest reached)** để chống gian lận.
   - **Xác thực tương tác:** Hộp thoại kiểm tra "Bạn có còn đang xem không?" xuất hiện định kỳ sau 15 phút không có hoạt động.

---

## 2. THIẾT KẾ CƠ SỞ DỮ LIỆU CORE (DATA MODELS TỐI ƯU)

Hệ thống được tái cấu trúc thành 4 Django Apps: `accounts`, `courses`, `tracking`, `assessments`.

```python
# ==========================================
# 1. APPS/ACCOUNTS: Người dùng, Vai trò & Hồ sơ
# ==========================================
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Học viên'),
        ('teacher', 'Giảng viên'),
        ('admin', 'Ban tổ chức / Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Mã sinh viên")
    class_name = models.CharField(max_length=50, blank=True, verbose_name="Lớp sinh hoạt")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    is_profile_completed = models.BooleanField(default=False, verbose_name="Đã hoàn tất thông tin cá nhân")

    def __str__(self):
        return f"{self.student_id or self.username} - {self.get_full_name() or self.username} ({self.get_role_display()})"


# ==========================================
# 2. APPS/COURSES: 3 Khóa học & Nội dung bài giảng
# ==========================================
class Course(models.Model):
    CODE_CHOICES = (
        ('WORD', 'Microsoft Word'),
        ('EXCEL', 'Microsoft Excel'),
        ('PPT', 'Microsoft PowerPoint'),
    )
    code = models.CharField(max_length=10, choices=CODE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructors = models.ManyToManyField(User, related_name='teaching_courses', limit_choices_to={'role': 'teacher'})
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    TYPE_CHOICES = (
        ('video', 'Video YouTube'),
        ('document', 'Tài liệu Google Drive'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    lesson_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='video')
    
    # Chỉ lưu ID gốc (Ví dụ: YouTube Video ID hoặc Google Drive File ID)
    external_id = models.CharField(max_length=255, help_text="YouTube Video ID hoặc Google Drive File ID")
    
    duration_seconds = models.PositiveIntegerField(default=0, help_text="Thời lượng video (giây)")
    min_watch_percent = models.PositiveIntegerField(default=80, help_text="Giảng viên quy định % tối thiểu để tính là hoàn thành bài")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['course', 'order']

    def __str__(self):
        return f"[{self.course.code}] Bài {self.order}: {self.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')


# ==========================================
# 3. APPS/TRACKING: Đo lường tiến độ xem Video
# ==========================================
class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progresses')
    
    furthest_second_reached = models.PositiveIntegerField(default=0, help_text="Mốc thời gian xem xa nhất (chặn tua vượt)")
    unique_watched_seconds = models.PositiveIntegerField(default=0, help_text="Tổng số giây xem thực tế không trùng lặp")
    completion_percentage = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

class WatchedInterval(models.Model):
    """Lưu lại các khoảng xem hợp lệ [start_sec, end_sec] để thuật toán gom khoảng tính % chính xác"""
    progress = models.ForeignKey(LessonProgress, on_delete=models.CASCADE, related_name='intervals')
    start_sec = models.PositiveIntegerField()
    end_sec = models.PositiveIntegerField()


# ==========================================
# 4. APPS/ASSESSMENTS: Google Forms Quiz & Xét Minh Chứng
# ==========================================
class FinalQuiz(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='final_quiz')
    title = models.CharField(max_length=200, default="Bài kiểm tra cuối khóa")
    google_forms_embed_url = models.URLField(help_text="Link nhúng Google Forms (có đuôi /viewform?embedded=true)")
    passing_score = models.FloatField(default=5.0, help_text="Điểm sàn đạt yêu cầu (thang 10)")
    max_score = models.FloatField(default=10.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Quiz - {self.course.title}"

class QuizSubmission(models.Model):
    quiz = models.ForeignKey(FinalQuiz, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    score = models.FloatField()
    is_passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user')
```

---

## 3. THIẾT KẾ ENGINE VIDEO TRACKER & CHỐNG GIAN LẬN

### 3.1. Hành vi của Trình phát Video (Frontend `tracker.js`)
1. **Kiểm soát thanh tua (Seek Control):**
   - Dùng biến `maxWatchedTime = progress.furthest_second_reached`.
   - Lắng nghe sự kiện `onStateChange` và kiểm tra liên tục qua `setInterval` mỗi 1 giây:
     - Nếu học viên tua về trước (`currentTime < maxWatchedTime`): **Cho phép bình thường** để ôn lại bài.
     - Nếu học viên cố tình kéo thanh tiến độ vượt quá vị trí xem xa nhất (`currentTime > maxWatchedTime + 3s`): **Lập tức gán lại `player.seekTo(maxWatchedTime, true)`** và hiển thị thông báo nhẹ: *"Bạn chỉ có thể tua lại phần đã học, không thể tua vượt bài mới."*
2. **Cơ chế Heartbeat tiết kiệm tài nguyên:**
   - Cứ mỗi 30 - 45 giây phát liên tục, gửi một gói JSON lên server:
     ```json
     {
       "lesson_id": 12,
       "interval": [120, 150],
       "current_time": 150
     }
     ```
   - Server chỉ cần cập nhật `furthest_second_reached` và chạy hàm `merge_intervals()` cực kỳ nhanh gọn.
3. **Modal "Bạn có còn đang xem không?" (Inactivity Prompt):**
   - Bộ đếm thời gian theo dõi sự kiện tương tác của người dùng (`mousemove`, `keydown`, `click`, `scroll`).
   - Nếu trong 15 phút người dùng không có bất kỳ tương tác nào:
     - Gọi `player.pauseVideo()`.
     - Hiện Popup chính giữa màn hình với âm thanh cảnh báo và đếm ngược 60 giây.
     - Nếu người dùng bấm *"Tôi vẫn đang xem"*: Tiếp tục phát video.
     - Nếu hết 60 giây không bấm: Tạm dừng gửi heartbeat để chống sinh viên bật máy treo đi ngủ.

---

## 4. QUY TRÌNH CHẤM ĐIỂM & ĐỒNG BỘ TỪ GOOGLE FORMS

1. Giảng viên tạo bài kiểm tra trên Google Forms (cài đặt chế độ Quiz để Google tự chấm trắc nghiệm).
2. **Quy ước bắt buộc trong Google Forms:**
   - Bật tùy chọn *"Thu thập địa chỉ email"*.
   - Câu hỏi số 1 bắt buộc: *"Nhập Mã số sinh viên (MSSV) của bạn:"*.
3. Khi hết hạn làm bài, Giảng viên vào Google Forms -> bấm **"Liên kết với Trang tính" (Google Sheets)** -> Tải file về dạng **Excel (`.xlsx`)** hoặc **CSV**.
4. Giảng viên truy cập LMS tại mục Quản lý khóa học -> Chọn **"Nhập bảng điểm Quiz"** -> Tải file Excel/CSV lên.
5. **Logic xử lý phía Backend (Django):**
   - Đọc dữ liệu các cột: `MSSV`, `Email`, `Điểm số`.
   - Tìm sinh viên theo thứ tự ưu tiên: Khớp theo `student_id` trước, nếu không thấy thì khớp theo `email`.
   - Quy đổi điểm về thang 10 (ví dụ: Google Form chấm 80/100 -> lưu vào hệ thống là 8.0).
   - So sánh với `passing_score` của khóa học để tự động đánh dấu `is_passed = (score >= passing_score)`.
   - Trả về báo cáo kết quả tức thì: *"Đã nhập điểm thành công cho 295/300 sinh viên. 5 trường hợp sai lệch MSSV (có danh sách cụ thể để kiểm tra tay)."*

---

## 5. CƠ CHẾ TEST PHÂN QUYỀN LINH HOẠT (CHO DEV & STAGING)

Để giúp team dev và tester có thể kiểm thử toàn bộ luồng hoạt động mà không cần setup Google OAuth phức tạp ngay từ đầu:

1. **Bộ tài khoản Mock (Seed Data Script):**
   - Viết sẵn lệnh quản lý: `python manage.py seed_test_data` tự động tạo:
     - 1 tài khoản Admin: `admin` / `admin123`
     - 2 tài khoản Giảng viên: `teacher_word` / `teacher123`, `teacher_excel` / `teacher123`
     - 5 tài khoản Sinh viên: `sv001` đến `sv005` (mật khẩu chung `sv123`) đã có sẵn MSSV.
     - Tạo sẵn 3 khóa học mẫu (Word, Excel, PPT) và các bài học demo video YouTube.
2. **Thanh chuyển vai trò nhanh (Role Switcher Toolbar):**
   - Trong môi trường `DEBUG = True`, đặt một thanh nhỏ ở góc dưới màn hình giúp Dev/Tester click chuyển nhanh giữa vai trò **Admin <-> Giảng viên <-> Học viên** mà không cần phải logout/login liên tục.

---

## 6. LỘ TRÌNH TRIỂN KHAI THEO 4 SPRINT (CORE MVP)

| Sprint | Thời gian | Mục tiêu bàn giao |
|---|---|---|
| **Sprint 1: Nền tảng, Auth & Phân quyền** | Tuần 1 | - Khởi tạo dự án Django, cấu hình PostgreSQL.<br>- Cài đặt `django-allauth` (Google SSO) + Form Onboarding nhập MSSV.<br>- Bộ phân quyền Role-based decorators.<br>- Script tạo tài khoản test phân quyền (`seed_test_data`). |
| **Sprint 2: Khóa học & Trình nhúng bài giảng** | Tuần 2 | - Tạo 3 khóa học: Word, Excel, PPT.<br>- Trang danh sách bài học và chi tiết bài học.<br>- Module chuẩn hóa URL YouTube/Drive an toàn + CSP.<br>- Tự động ghi danh sinh viên vào 3 khóa. |
| **Sprint 3: Video Tracking Engine** | Tuần 3 | - Tích hợp YouTube IFrame API.<br>- Thuật toán chặn tua vượt mốc, cho phép tua lùi.<br>- Cơ chế gửi heartbeat định kỳ 30s-45s + Merge Intervals.<br>- Cấu hình % hoàn thành theo từng bài giảng.<br>- Popup tương tác chống treo máy sau 15 phút. |
| **Sprint 4: Google Forms Quiz & Dashboard Xét Minh Chứng** | Tuần 4 | - Nhúng Google Forms vào bài thi cuối khóa.<br>- Module import bảng điểm Excel/CSV từ Google Sheets, tự động khớp MSSV/Email.<br>- Trang tổng hợp kết quả (Review Dashboard) cho BTC.<br>- Xuất danh sách 300 sinh viên đạt điều kiện cấp minh chứng ra file Excel.<br>- Deploy production lên VPS (Nginx, Gunicorn, SSL). |
