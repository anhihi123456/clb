# o365_LMS - Hệ Thống Quản Lý Học Tập Khóa Kỹ Năng Mềm

Hệ thống quản lý học tập (LMS) tinh gọn, chuyên dụng phục vụ các khóa đào tạo Tin học văn phòng & Kỹ năng mềm (Word, Excel, PowerPoint) của **Câu lạc bộ Tin học & Office 365 (CLB o365)**.

---

## 🚀 Tính năng nổi bật

- **Phân quyền người dùng (RBAC):** 3 vai trò Học viên (Student), Giảng viên (Teacher), Ban tổ chức (Admin).
- **Bộ nhúng học liệu an toàn (Safe Embed Engine):**
  - Giảng viên chỉ cần dán link thường từ **YouTube**, **Google Drive (PDF/Slide)** hoặc **Google Forms**.
  - Backend tự động bóc tách ID, chuẩn hóa link nhúng và ngăn chặn hoàn toàn tấn công chèn mã độc (XSS).
- **Tính năng Xem trước nhúng trực tiếp (Live Embed Preview):**
  - Trình duyệt hiển thị ngay khung phát video hoặc tài liệu PDF ngay khi giảng viên nhập link trước khi lưu.
- **Giao diện học tập hiện đại:** Tương thích di động (Mobile responsive), tích hợp dự phòng mở tài liệu tab mới nếu bị chặn cookie.
- **Tiện ích Kiểm thử nhanh (DEV Role Switcher):** Thanh công cụ 1-chạm giúp chuyển đổi tức thì giữa các tài khoản mẫu (`teacher_word`, `teacher_excel`, `sv001`, `admin`) mà không cần đăng nhập lại.

---

## 🛠️ Công nghệ sử dụng

- **Backend:** Python 3.11+, Django 5.x / 6.x
- **Frontend:** Django Templates + Tailwind CSS + FontAwesome Icons
- **Database:** SQLite (Môi trường Phát triển) / PostgreSQL (Môi trường Production)
- **Hạ tầng lưu trữ:** Tận dụng YouTube Unlisted (Video), Google Drive (PDF/Slide) và Google Forms (Bài kiểm tra) giúp tối ưu 100% dung lượng máy chủ VPS.

---

## 📦 Cài đặt & Chạy thử nghiệm cục bộ

### 1. Yêu cầu hệ thống
- Đã cài đặt **Python 3.11+** và **Git**.

### 2. Cài đặt các gói phụ thuộc
```bash
# Khởi tạo và kích hoạt môi trường ảo (khuyến nghị)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường
Tạo tệp `.env` từ tệp mẫu:
```bash
cp .env.example .env
```

### 4. Chạy migration và nạp dữ liệu mẫu
```bash
# Áp dụng cơ sở dữ liệu
python manage.py migrate

# Khởi tạo dữ liệu mẫu và tài khoản test phân quyền
python manage.py seed_test_data
```

### 5. Khởi động máy chủ
```bash
python manage.py runserver
```
Mở trình duyệt và truy cập: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👤 Danh sách tài khoản thử nghiệm (Seed Data)

| Vai trò | Tên đăng nhập | Mật khẩu | Mô tả nhiệm vụ |
|---|---|---|---|
| **Giảng viên Word** | `teacher_word` | `teacher123` | Quản lý & thiết lập bài giảng khóa Word |
| **Giảng viên Excel** | `teacher_excel` | `teacher123` | Quản lý & thiết lập bài giảng khóa Excel |
| **Học viên** | `sv001` | `sv123` | MSSV: `20210001` (Lớp CNTT-01) |
| **Ban tổ chức (Admin)** | `admin` | `admin123` | Toàn quyền quản trị hệ thống và Django Admin |

*Lưu ý: Có thể dùng thanh DEV TOOLBAR ở đầu trang để chuyển đổi vai trò 1-chạm.*

---

## 🔒 Hướng dẫn An toàn Bảo mật (Security Checklist)

- **Không bao giờ commit tệp `.env` hoặc `db.sqlite3`** lên repository công khai.
- **Khi triển khai Production:**
  - Đặt `DJANGO_DEBUG=False` trong `.env`.
  - Thiết lập một chuỗi ngẫu nhiên dài cho `DJANGO_SECRET_KEY`.
  - Cấu hình chính xác tên miền vào `DJANGO_ALLOWED_HOSTS`.

