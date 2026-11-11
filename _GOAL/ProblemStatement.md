
CLB o365 đang tổ chức một khóa KNM cho sinh viên. Số lượng sinh viên tham gia là khoảng 300 sinh viên 
Tiêu chí đánh giá hiện tại của khóa là quá trình tham gia lớp học (offline và xem video online) và làm bài kiểm tra cuối khóa.
Tuy vậy trong những kì trước clb gặp các vướng mắc sau:

### Về phía câu lạc bộ:
- Đối với những buổi học offline: Khó khăn trong việc quản lí điểm danh trực tiếp, có xảy ra trường hợp điểm danh hộ
- Đối với buổi học online: Khó khăn trong việc quản lí số lượt xem video, cũng như việc đảm bảo sinh viên xem hết video hay không.

### Về phía học sinh:
- Khó khăn trong việc theo dỗi tiến độ và thông tin của khóa học
- Bất tiện trong việc xin phép nghỉ học, xin tài liệu.

*Điều này dẫn đến Clb gặp khó khăn trong việc đánh giá và cấp minh chứng.*

### Giới hạn kĩ thuật + cách khắc phục
- Tài nguyên hạn chế, dung lượng VPS rất ít (không thể lưu trữ database của 300 học viên + các giảng viên + admin)

### Cách khắc phục: 
- Authentication Có thể sử dụng API của Google (Sign in with Google) hoặc Firebase (phù hợp cho dưới 100 người). Hoặc là nếu dùng được đăng nhập bằng tài khoản nhà trường (chưa biết cách)
    - Triển khai: Google sẽ lo authentication nhưng sẽ vẫn phải làm chức năng phân quyền (ít dữ liệu hơn cho database)
- Phân quyền: .................................................................................... chắc chắn cần database
- Các Course Material sẽ là embed từ video youtube, link google drive và MS form cho quizzi và test.
    - Triển khai: Sử dụng iframe để embed và lấy data trực tiếp từ source
    Problem according to Claude
    Summary

## Kế hoạch triển khai phần Core (MVP)
- **Học viên:** Đăng nhập Google, cập nhật MSSV, xem 3 khóa học (Word, Excel, PPT), xem video bài giảng với trình player chống tua, làm bài kiểm tra Google Forms, xem tiến độ hoàn thành.
- **Giảng viên:** Đăng nhập, đưa link bài giảng (YouTube, Drive), cấu hình % hoàn thành bài học, nhúng Google Forms và tải file Excel điểm để cập nhật kết quả.
- **Admin / Ban tổ chức:** Quản lý người dùng, phân quyền (Học viên, Giảng viên, Admin), xem bảng tổng hợp kết quả 300 sinh viên và xuất danh sách đủ điều kiện cấp minh chứng.

- Student tracking: Vì mình embed form nên có thể xuất luôn ra riêng xong làm gì đó với cái đó
    Triển khai: Xuất excel sau deadline của quizzi + điểm danh theo ictsv 
## Kê hoạch triển khai
### Core cần có
#### Học sinh 
- Đăng nhập
- Course (chưa cần có nội dung nhưng có 3 course PPT, Excel, Word). 
- Quizz
#### Giáo viên
- Đăng nhập
- Đăng tài liệu (bằng cách embed link)
- Tạo quizzi
#### Admin
- Đăng nhập
- Phân quyền : học sinh, giáo viên, admin
- Phân course: học sinh giáo viên vào course nào.
#### Một số chức năng phụ (đăng trưng)
- Track tương tác youtube video, "bạn có còn xem video này?"
- Điểm danh ictsv 

### Phụ
- Đăng announcement, notification
- Dashboard
- Progress tracker for student

