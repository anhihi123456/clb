# Công nghệ sử dụng cho LMS

Tài liệu kỹ thuật · Ngày 10/11/2026 · Quy mô: lớp học  300 người dùng

## 1. Mục tiêu và phạm vi

Xây dựng một hệ thống quản lý học tập (LMS) nhẹ cho lớp học nhỏ. Hệ thống tập trung vào phần cốt lõi (khóa học, bài học, ghi danh, tiến độ, phân quyền, bảng điểm) và tận dụng dịch vụ có sẵn cho phần nặng (video, tài liệu, bài kiểm tra, đăng nhập).

**Ngoài phạm vi ở giai đoạn đầu:** đa tổ chức (multi-tenant), SCORM/xAPI, thanh toán, danh sách chờ, báo cáo tuân thủ.

## 2. Các quyết định công nghệ đã chốt

| Hạng mục | Lựa chọn | Lý do chính |
| --- | --- | --- |
| Backend | Django (Python) | Có sẵn xác thực, trang admin, ORM, form; hợp kỹ năng Python hiện có |
| Cơ sở dữ liệu | PostgreSQL | Dữ liệu quan hệ (ghi danh, điểm, tiến độ), truy vấn báo cáo tốt |
| Đăng nhập | Google (OpenID Connect) qua `django-allauth` | Không lưu mật khẩu, có sẵn 2FA của Google |
| Video | YouTube (unlisted) + IFrame Player API | Miễn phí, không tốn dung lượng VPS, theo dõi được sự kiện phát |
| Lưu trữ tài liệu | Google Drive (PDF, slide) nhúng bằng iframe | Cùng hệ sinh thái với đăng nhập Google |
| Bài kiểm tra | Microsoft Forms nhúng bằng iframe | Tự chấm điểm, không cần tự xây engine quiz |
| Giao diện | HTML/CSS/JS + Bootstrap hoặc Tailwind, render phía server | Đơn giản, đủ cho quy mô này |
| Hosting | VPS nhỏ (Linux) | Chi phí cố định, kiểm soát hoàn toàn |

## 3. Kiến trúc tổng quan

Kiến trúc là một ứng dụng Django duy nhất (modular monolith), tích hợp dịch vụ ngoài:

```
Trình duyệt học viên / giảng viên
        │  HTTPS
        ▼
   Nginx (reverse proxy, HTTPS)
        │
        ▼
   Gunicorn + Django
   ├─ accounts   (người dùng, vai trò, đăng nhập Google)
   ├─ courses    (khóa học, bài học)
   ├─ enrollments (ghi danh)
   ├─ progress   (tiến độ, theo dõi video)
   ├─ assessments (liên kết bài kiểm tra, điểm)
   └─ notifications (email, thông báo)
        │
        ▼
   PostgreSQL

Dịch vụ ngoài: Google (đăng nhập, Drive), YouTube (video), Microsoft Forms (bài kiểm tra)
```

Nội dung nặng (video, file) nằm ở dịch vụ ngoài; VPS chỉ lưu dữ liệu của chính LMS.

## 4. Chi tiết từng thành phần

### 4.1 Django và PostgreSQL

- Dùng phiên bản Django LTS mới nhất (kiểm tra trên djangoproject.com) và Python tương thích.
- Chia ứng dụng thành các app nhỏ theo module ở sơ đồ trên, mỗi app có model, view và test riêng.
- Dùng SQLite khi phát triển, PostgreSQL khi triển khai thật; cấu hình qua biến môi trường.
- Dùng trang Django admin cho các thao tác quản trị (gán vai trò, xem ghi danh) thay vì tự viết giao diện admin.
- Chạy `python manage.py clearsessions` định kỳ bằng cron để xóa phiên hết hạn.

### 4.2 Đăng nhập bằng Google

- Dùng `django-allauth` với Google provider (OpenID Connect).
- Lưu `sub` của Google làm định danh cố định, không dùng email làm khóa chính; chỉ tin email khi `email_verified` là true.
- Giới hạn tài khoản của trường: tham số `hd` chỉ là gợi ý phía trình duyệt, nên **bắt buộc kiểm tra lại tên miền email ở phía server** (ví dụ trong adapter của allauth) hoặc dùng danh sách email được phép.
- Giữ `SOCIALACCOUNT_STORE_TOKENS = False` (mặc định) vì chỉ dùng Google để đăng nhập, không gọi API khác.
- Vai trò (student, teacher, admin) lưu trong bảng User của LMS. Người dùng mới mặc định là student; admin nâng quyền giảng viên trong trang Django admin.
- Mỗi view đều phải kiểm tra quyền: học viên chỉ thấy khóa học đã ghi danh, giảng viên chỉ sửa khóa học của mình.

### 4.3 Video YouTube

- Dùng chế độ **Unlisted** (không dùng Private vì học viên không mở được). Chỉ lưu video ID trong cơ sở dữ liệu và tự dựng URL `https://www.youtube.com/embed/VIDEO_ID`.
- Dùng YouTube IFrame Player API để theo dõi: play, pause, kết thúc, tốc độ phát, và phát hiện tua bằng cách so sánh `getCurrentTime()` mỗi giây.
- Gửi dữ liệu về server theo chu kỳ 30-60 giây và khi pause/seek/kết thúc (không gửi quá dày), kèm trạng thái tab ẩn/hiện qua Page Visibility API.
- Lưu **các đoạn đã xem** (ví dụ 0-120 giây, 300-480 giây) để tính phần trăm xem thật; đánh dấu hoàn thành khi đạt ngưỡng (ví dụ 90%).
- Nhắc "Bạn còn xem không?" tự xây bằng bộ đếm giờ và hộp thoại; không phát hiện được thao tác bên trong iframe.
- **Giới hạn:** không theo dõi được khi xem trong app YouTube hoặc Picture-in-Picture; dữ liệu phía client có thể bị làm giả, nên với nội dung quan trọng hãy kèm một bài kiểm tra ngắn.

### 4.3 Google Drive (PDF, slide)

- Nhúng PDF bằng liên kết dạng `https://drive.google.com/file/d/FILE_ID/preview`; không dùng liên kết xem hay tải thông thường vì không nhúng được.
- Google Slides dùng liên kết `/embed` hoặc `/preview`.
- Cài đặt chia sẻ:
  - "Bất kỳ ai có liên kết": dễ dùng nhưng liên kết có thể bị chia sẻ ra ngoài.
  - "Giới hạn trong tổ chức": an toàn hơn, nhưng học viên phải đăng nhập đúng tài khoản Google của trường.
- Luôn kèm nút "Mở trong tab mới" phòng trường hợp trình duyệt chặn cookie bên thứ ba.
- LMS không đọc được việc học viên đã xem tài liệu hay chưa, nên cần nút "Đánh dấu hoàn thành" thủ công.

### 4.4 Bài kiểm tra bằng Microsoft Forms

- Tạo bài ở chế độ quiz để tự chấm điểm, rồi lấy mã nhúng qua **Share > Embed**.
- **Lưu ý quan trọng về tài khoản:** Microsoft Forms thường yêu cầu đăng nhập bằng tài khoản Microsoft nếu giới hạn người trả lời trong tổ chức, trong khi LMS đăng nhập bằng Google. Học viên có thể phải có cả hai tài khoản, và việc đăng nhập Microsoft bên trong iframe có thể lỗi. Cần xác nhận với IT của trường trước khi quyết định cách dùng, và luôn có nút "Mở bài kiểm tra trong tab mới".
- **Đưa điểm về LMS** (Forms không tự gửi điểm sang ứng dụng của bạn). Các cách, từ đơn giản đến phức tạp:
  1. Giảng viên xuất kết quả sang Excel rồi nhập vào LMS bằng CSV (đủ cho phiên bản đầu).
  2. Dùng Power Automate gửi kết quả mỗi lần có bài nộp tới một endpoint của LMS (một số tính năng của Power Automate có thể cần giấy phép riêng, cần kiểm tra).
  3. Đọc kết quả qua Microsoft Graph API theo lịch (phức tạp hơn, cần đăng ký ứng dụng và quyền).
- Khớp học viên bằng email: chỉ chính xác nếu học viên dùng cùng một địa chỉ email của trường ở cả Google và Microsoft.
- **Hạn chế:** không phát hiện chuyển tab, không chống sao chép; phù hợp bài luyện tập hơn là thi quan trọng.

### 4.5 Giao diện

- Render phía server bằng template Django, thêm JavaScript cho phần cần tương tác (trình phát video, tiến độ).
- Dùng Bootstrap hoặc Tailwind để giao diện sạch và responsive; chú ý nhãn form, độ tương phản và điều hướng bàn phím (truy cập được).
- Hai màn hình quan trọng nhất: trang khóa học của học viên và trình soạn khóa học của giảng viên.

### 4.6 Hosting và vận hành

- VPS Linux khoảng 20-25 GB là đủ vì video và file nằm ở dịch vụ ngoài.
- Stack triển khai: Nginx + Gunicorn + PostgreSQL, HTTPS bằng Let's Encrypt (Certbot), quản lý tiến trình bằng systemd.
- Biến môi trường cho khóa bí mật (Google client secret, `SECRET_KEY`, mật khẩu cơ sở dữ liệu); **không đưa vào Git**.
- Sao lưu tự động bằng `pg_dump` theo lịch (cron), lưu bản sao ngoài VPS; thử khôi phục định kỳ.
- Xoay vòng log để không đầy ổ đĩa.

## 5. Mô hình dữ liệu khởi đầu

```
User (google_sub, email, name, role)
Course (title, description, teacher)
Enrollment (user, course, created_at)
Lesson (course, title, order, type, provider, external_id_or_url, published)
LessonProgress (user, lesson, completed_at)
WatchedSegment (user, lesson, start_sec, end_sec)
VideoEvent (user, lesson, type, position, created_at)
QuizLink (lesson, form_url, max_score)
QuizResult (user, quiz_link, score, submitted_at)
Announcement (course, title, body, created_at)
```

Trong đó `Lesson.type` nhận các giá trị video, document, quiz, text và `Lesson.provider` nhận youtube, gdrive, msforms.

## 6. Bảo mật

- **Không nhúng HTML thô** do giảng viên dán vào. Giảng viên dán liên kết thường, backend tự rút ID và dựng URL nhúng, chỉ cho phép các tên miền định sẵn (youtube.com, drive.google.com, docs.google.com, forms.office.com...).
- Thêm Content Security Policy với `frame-src` chỉ gồm các tên miền trên.
- Kiểm tra quyền trên mọi view và viết test cho logic phân quyền; học viên không bao giờ thấy điểm hay bài nộp của người khác.
- Bật CSRF, HTTPS, cookie an toàn (`Secure`, `HttpOnly`), và cập nhật phụ thuộc thường xuyên.
- Quyền riêng tư: chỉ lưu dữ liệu cần thiết (sub, email, tên), cho phép xuất và xóa dữ liệu khi được yêu cầu.

## 7. Rủi ro và điểm cần lưu ý

| Rủi ro | Mức độ | Cách xử lý |
| --- | --- | --- |
| Học viên cần cả tài khoản Google và Microsoft cho bài kiểm tra | Cao | Hỏi IT sớm; luôn có nút mở tab mới; cân nhắc tự xây quiz đơn giản về sau |
| Điểm từ Microsoft Forms không tự về LMS | Trung bình | Bắt đầu bằng nhập CSV, sau đó tự động hóa |
| Liên kết Drive bị xóa hoặc đổi quyền | Trung bình | Nút "báo lỗi nội dung"; quy ước sở hữu file thuộc tài khoản của trường |
| Dữ liệu theo dõi video bị làm giả | Thấp (quy mô nhỏ) | Kèm bài kiểm tra ngắn sau video |
| Phụ thuộc chính sách của Google, YouTube, Microsoft | Trung bình | Lưu liên kết gốc, giữ kiến trúc dễ đổi nhà cung cấp |

## 8. Lộ trình triển khai

1. **Nền tảng (1 tuần):** Git, hướng dẫn chính thức của Django, SQL cơ bản.
2. **Người dùng và vai trò (1 tuần):** đăng nhập Google, vai trò mặc định student, kiểm tra tên miền ở server.
3. **Khóa học và bài học (1-2 tuần):** mô hình Course/Lesson, trình chuyển liên kết thành mã nhúng với danh sách tên miền cho phép.
4. **Ghi danh và tiến độ (1-2 tuần):** mã tham gia khóa học, nút hoàn thành, thanh tiến độ.
5. **Theo dõi video (1-2 tuần):** gửi dữ liệu theo lô, đoạn đã xem, nhắc "còn xem không".
6. **Bài kiểm tra (1 tuần):** nhúng Microsoft Forms, nhập điểm bằng CSV, bảng điểm cho giảng viên.
7. **Thông báo và hoàn thiện (1-2 tuần):** thông báo, email, giao diện responsive, HTTPS, sao lưu, thử với người dùng thật.

Nên phát hành bản tối thiểu sau bước 4 để lấy phản hồi sớm.

## 9. Việc cần làm tiếp theo

- Hỏi IT của trường: học viên có tài khoản Microsoft để làm Forms không, chính sách chia sẻ Drive, và có cho phép đăng ký ứng dụng Google OAuth hay không.
- Tạo dự án Google Cloud, cấu hình màn hình đồng ý OAuth và Client ID.
- Khởi tạo dự án Django, kết nối PostgreSQL và cài `django-allauth`.
- Viết model đầu tiên: User, Course, Lesson, Enrollment.
