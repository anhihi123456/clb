# LMS Research
## LMS là gì?
LMS (Learning Management System) là hệ thống quản lí học tập được thiết kế cho các nhà trường, doanh nghiệp, tổ chức, nhằm quản lý đào tạo và phát triển nguồn nhân lực. 
## LMS cần có những tính năng gì?
- Định danh và phân quyền: người dùng, vai trò (học viên, giảng viên, quản trị viên), tổ chức/đơn vị thuê (tenant), đăng nhập một lần SSO (SAML, OIDC), quyền hạn. 
- Quản lý nội dung: khóa học, học phần (module), bài học, đa phương tiện (video, PDF, gói SCORM/xAPI), quản lý phiên bản.
- Quản lý khóa học: ai được truy cập nội dung nào, nhóm lớp (cohort), điều kiện tiên quyết, danh sách chờ, thời hạn truy cập.
- Theo dõi tiến độ: trạng thái hoàn thành, thời gian học, vị trí học dở (để tiếp tục), chứng chỉ.
- Đánh giá: bài kiểm tra trắc nghiệm, bài tập, chấm điểm, ngân hàng câu hỏi, tiêu chí chấm (rubric), giới hạn số lần làm bài.
- Giao tiếp: thông báo của lớp, diễn đàn thảo luận, thông báo đẩy/email.
- Báo cáo và phân tích: tiến độ học viên, hiệu quả khóa học, báo cáo tuân thủ.
- Thương mại (tùy chọn): thanh toán, đăng ký theo gói, mã giảm giá.
## Một trang LMS cần có gì?
### Học sinh 
- Account: Login, logout, password reset, profile,....  
- Courses and learning:
    - Dashbroad > Course > Lesson st    ure 
    - Class Material,es    sment
    - Progress and mark tracking
- Communication: Anouncement, certificate.


### Giáo viên
- Student Management: Teacher enrolls students (or students join with a code).
- Course Management: 
    - File uploads for materials (PDFs, slides).
    - Create Quizzes with multiple choice, auto-graded.
    - Assignment submissions (file upload) with teacher grading and feedback.
- Assessment: Progress track for student completion.
### Admin

- Users and roles
    - View and search all users
    - Assign or change roles (promote student to teacher)
    - Deactivate or delete accounts
    - Allowlist of emails or domains allowed to sign in

- Oversight:
    - View, edit, or archive any course
    - Reassign a course to another teacher
    - View all enrollments

- System:
    - Site settings (name, logo, email sender, authentication providers)
    - Email notification configuration
    - Audit log of important actions (role changes, grade edits, deletions) (later)
    - Backup and restore, storage usage monitoring
    - Data export and deletion on request (privacy)
