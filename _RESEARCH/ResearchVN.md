# Hệ Thống Quản Lý Học Tập (LMS) - Tài Liệu Nghiên Cứu & Yêu Cầu Tính Năng

## 1. LMS là gì?
**LMS (Learning Management System - Hệ thống quản lý học tập)** là nền tảng phần mềm được xây dựng nhằm lên kế hoạch, triển khai, quản lý và đánh giá toàn diện quá trình dạy và học. LMS phục vụ các trường học, viện đào tạo, doanh nghiệp và tổ chức giáo dục bằng cách cung cấp một không gian số tập trung: giúp giảng viên truyền tải bài giảng, theo dõi tiến độ và chấm điểm; đồng thời giúp học viên tiếp cận tri thức linh hoạt, cộng tác và phát triển năng lực cá nhân.

---

## 2. LMS cần có những tính năng cốt lõi gì?
Một hệ thống LMS chuẩn doanh nghiệp và giáo dục hiện đại cần đáp ứng các nhóm năng lực sau:
- **Định danh & Phân quyền (IAM):** Kiến trúc đa người thuê (multi-tenant), phân cấp vai trò người dùng (Học viên, Giảng viên/Giáo viên, Trợ giảng, Quản trị viên), hỗ trợ đăng nhập một lần SSO (Microsoft Entra ID / Office 365, Google Workspace, SAML 2.0, OpenID Connect) và cơ chế phân quyền dựa trên vai trò (RBAC).
- **Quản lý nội dung đào tạo:** Tổ chức cấu trúc phân cấp (Khóa học > Học phần/Chương > Bài học/Chủ đề), hỗ trợ định dạng đa phương tiện (video, tài liệu PDF, bài trình chiếu, âm thanh, gói bài giảng chuẩn SCORM 1.2/2004, xAPI), quản lý phiên bản tài liệu và liên kết kho lưu trữ đám mây (OneDrive, SharePoint).
- **Quản lý khóa học & Ghi danh:** Phân lớp/nhóm học (cohort), kiểm soát phương thức ghi danh (tự do, phê duyệt, dùng mã truy cập/join code), quy định điều kiện tiên quyết (prerequisites), thời hạn truy cập khóa học và danh sách chờ.
- **Theo dõi tiến độ & Lộ trình học:** Cơ chế tự động ghi nhận hoàn thành bài học, đo lường thời gian xem video thực tế, lưu điểm dừng phát video (để học tiếp tục), danh sách kiểm tra (checklist) và tự động cấp chứng chỉ.
- **Đánh giá & Khảo sát:** Bộ công cụ tạo bài tập nộp file, bài trắc nghiệm tự động chấm điểm, ngân hàng câu hỏi, ma trận tiêu chí chấm điểm (rubric), quy chế chống gian lận (giới hạn thời gian, xáo trộn câu hỏi/đáp án, phát hiện chuyển tab) và chính sách nộp lại.
- **Tương tác & Giao tiếp:** Bảng tin thông báo lớp học, diễn đàn hỏi đáp theo chủ đề/bài giảng, nhắn tin trao đổi trực tiếp, phòng học ảo trực tuyến (tích hợp Microsoft Teams, Zoom).
- **Báo cáo & Phân tích học tập (Analytics):** Bảng tổng hợp tiến độ học viên, biểu đồ phổ điểm, cảnh báo học viên có nguy cơ trễ hạn/bỏ học, tỷ lệ hoàn thành khóa học và báo cáo tuân thủ đào tạo.
- **Mở rộng & Thương mại hóa (Tùy chọn):** Cổng thanh toán trực tuyến, gói đăng ký học định kỳ, mã ưu đãi và hệ thống API kết nối mở rộng (REST/GraphQL).

---

## 3. Chi tiết tính năng LMS theo vai trò người dùng

### 3.1. Phân hệ Học sinh / Học viên (Student / Learner)

#### A. Tài khoản, Định danh & Hồ sơ cá nhân
- **Đăng nhập linh hoạt & Hiện đại:** Đăng nhập thông qua tài khoản trường/doanh nghiệp (Microsoft 365 SSO, Google) hoặc email mật khẩu truyền thống, xác thực đa yếu tố (MFA), lấy lại mật khẩu an toàn.
- **Quản lý hồ sơ:** Cập nhật ảnh đại diện (avatar), tên hiển thị, thông tin liên hệ, tiểu sử, tùy chọn ngôn ngữ hiển thị và múi giờ học tập.
- **Tùy chỉnh thông báo cá nhân:** Cài đặt kênh nhận thông báo (thông báo trong ứng dụng, email định kỳ, thông báo đẩy) khi có bài tập mới, bài thi sắp mở hoặc giáo viên đã công bố điểm số.
- **Bảo mật phiên đăng nhập:** Quản lý các thiết bị đang đăng nhập và lịch sử phiên hoạt động.

#### B. Bảng điều khiển (Dashboard) & Điều hướng học tập
- **Dashboard cá nhân hóa:**
  - Danh thiếp trực quan các khóa học của tôi: Khóa đang học, khóa đã hoàn thành, khóa đã lưu trữ, đi kèm thanh phần trăm (%) tiến độ trực quan.
  - Phím tắt **"Tiếp tục học"**: Tự động chuyển ngay đến bài học gần nhất đang học dở.
- **Lịch học tập tổng hợp (Academic Calendar):** Đồng bộ hóa tất cả hạn nộp bài tập, thời gian mở/đóng bài thi trắc nghiệm, các buổi học trực tuyến qua Teams và lịch nghỉ.
- **Danh sách nhiệm vụ cần làm (To-Do List):** Liệt kê công việc theo mức độ ưu tiên và thời hạn (đến hạn hôm nay, trong tuần này, quá hạn).

#### C. Trải nghiệm bài học & Tương tác nội dung
- **Trình duyệt khóa học phân tầng:** Cấu trúc phân cấp mạch lạc: Đề cương môn học > Chương/Module > Bài học > Tài liệu đính kèm.
- **Trình phát đa phương tiện tối ưu:**
  - Trình phát video chuyên nghiệp hỗ trợ tua tốc độ (0.5x - 2x), phụ đề (captions), đánh dấu mốc thời gian (bookmark) và tự động ghi nhớ vị trí đang xem.
  - Trình đọc tài liệu tích hợp: Xem trực tiếp file PDF, slide thuyết trình và nhúng các tệp Microsoft Office 365 (Word, Excel, PowerPoint online) ngay trên trình duyệt mà không cần tải về máy.
  - Hỗ trợ các gói nội dung tương tác chuẩn SCORM / HTML5.
- **Tài liệu tham khảo tải về:** Dễ dàng tải tài liệu bổ trợ, mã nguồn mẫu, bảng tóm tắt kiến thức và đề cương ôn tập.
- **Ghi chú cá nhân trong bài học:** Tạo ghi chú riêng tư gắn liền với mốc thời gian video hoặc đoạn văn bản; hỗ trợ xem lại và xuất file ghi chú cá nhân.

#### D. Nộp bài tập & Bài tập thực hành (Assignments)
- **Thông tin bài tập chi tiết:** Nắm rõ hướng dẫn đề bài, file đề đính kèm, thang điểm tối đa, hạn nộp chính thức, thời gian cho phép nộp muộn (nếu có) và bảng tiêu chí chấm điểm (rubric).
- **Hình thức nộp bài đa dạng:**
  - Tải lên tệp (nhiều tệp, kéo thả, giới hạn định dạng file như PDF, DOCX, ZIP và giới hạn dung lượng).
  - Trình soạn thảo văn bản trực tiếp (Rich Text).
  - Dán liên kết ngoài (link sản phẩm dự án, GitHub repo, Figma) hoặc chọn tệp trực tiếp từ đám mây (OneDrive, Google Drive).
- **Lịch sử & Trạng thái nộp:** Xác nhận trạng thái đã nộp thành công, thời gian nộp, lưu lại lịch sử các phiên bản nộp và cho phép nộp lại bài khi còn trong hạn.
- **Xem phản hồi & Điểm chi tiết:** Xem nhận xét trực tiếp từ giáo viên, chú thích ghi trên bài nộp, file chấm trả về và điểm chi tiết theo từng tiêu chí trong rubric.

#### E. Bài kiểm tra trắc nghiệm & Thi trực tuyến (Quizzes & Exams)
- **Đa dạng các dạng câu hỏi:** Trắc nghiệm 1 đáp án, trắc nghiệm nhiều đáp án, Đúng/Sai, điền vào chỗ trống, nối cột tương ứng, sắp xếp thứ tự và câu hỏi tự luận ngắn.
- **Không gian làm bài thi chuẩn hóa:**
  - Đồng hồ đếm ngược thời gian thực, tự động thu bài khi hết giờ.
  - Bảng điều hướng câu hỏi: Dễ dàng xem câu đã làm, chưa làm, đánh dấu cờ (flag) để kiểm tra lại trước khi nộp.
  - Tự động lưu đáp án liên tục về máy chủ nhằm chống mất bài khi mất kết nối mạng bất ngờ.
- **Xem lại kết quả & Giải thích:** Xem điểm số ngay (đối với câu trắc nghiệm tự động), xem lời giải chi tiết và đáp án đúng (tùy theo cấu hình mở đáp án của giáo viên).
- **Theo dõi lượt làm bài:** Xem số lượt làm bài còn lại, lịch sử điểm số các lần trước và quy tắc lấy điểm (lấy điểm cao nhất hay điểm lần cuối).

#### F. Sổ điểm, Tiến độ & Đánh giá năng lực
- **Sổ điểm cá nhân (Gradebook):** Hiển thị chi tiết danh sách đầu điểm, trọng số điểm (chuyên cần, bài tập về nhà, giữa kỳ, cuối kỳ), điểm số đạt được, điểm trung bình lớp (nếu được mở) và điểm tổng kết quy đổi (hệ 10, hệ 4, điểm chữ).
- **Theo dõi tiến độ học tập:** Bảng danh mục công việc đã hoàn thành, tỉ lệ % hoàn tất khóa học và tổng số giờ đã học.
- **Bản đồ năng lực (Skills/Competencies):** Biểu đồ thể hiện mức độ làm chủ các chuẩn đầu ra của môn học.

#### G. Giao tiếp & Tương tác cộng đồng
- **Kênh thông báo môn học:** Cập nhật tức thời thông báo khẩn, lịch thay đổi từ giáo viên kèm bản sao gửi về email cá nhân.
- **Diễn đàn hỏi đáp & Thảo luận (Q&A Forum):** Đặt câu hỏi theo từng bài học, bình chọn (upvote) câu hỏi/câu trả lời hữu ích, trả lời theo luồng (thread) và xem các câu trả lời được giáo viên duyệt chuẩn (Teacher Approved).
- **Nhắn tin trực tiếp & Nhóm học tập:** Trò chuyện, trao đổi học tập với giáo viên, trợ giảng hoặc các bạn trong nhóm làm dự án.
- **Lớp học ảo trực tuyến:** Bấm tham gia trực tiếp vào buổi học trực tuyến qua Microsoft Teams hoặc Zoom được lên lịch sẵn từ thời khóa biểu khóa học.

#### H. Chứng chỉ & Động lực học tập
- **Cấp chứng chỉ tự động:** Nhận chứng chỉ hoàn thành khóa học bản PDF có mã định danh/QR Code xác thực ngay khi hoàn thành đầy đủ các tiêu chí tiên quyết.
- **Chia sẻ mạng xã hội:** Chia sẻ chứng nhận trực tiếp lên hồ sơ LinkedIn hoặc tải về lưu trữ trong hồ sơ năng lực cá nhân.

---

### 3.2. Phân hệ Giáo viên / Giảng viên (Teacher / Instructor)

#### A. Thiết kế khóa học & Quản trị giáo trình
- **Bộ công cụ xây dựng khóa học trực quan (Course Builder):** Dễ dàng kéo thả, sắp xếp cấu trúc chương mục, bài học và các mốc học tập.
- **Trình soạn thảo bài giảng mạnh mẽ (WYSIWYG):** Hỗ trợ viết định dạng Markdown, công thức toán học LaTeX, khối mã nguồn (code blocks), nhúng video và bảng biểu.
- **Lộ trình mở bài học linh hoạt (Drip Feeding):**
  - Mở bài học tự động theo lịch hẹn ngày/giờ.
  - Thiết lập điều kiện mở khóa bài (ví dụ: Phải hoàn thành Bài kiểm tra chương 1 đạt từ 80% trở lên mới được mở Bài học chương 2).
- **Kho học liệu số & Tích hợp đám mây:**
  - Tải lên hàng loạt tài liệu bài giảng, slide PowerPoint, tài liệu PDF, video bài giảng.
  - Tích hợp trực tiếp với đám mây Microsoft OneDrive / SharePoint / Google Drive giúp chèn tài liệu nhanh chóng.
- **Thiết lập & Điều phối khóa học:** Bật/tắt trạng thái phát hành (Draft/Published), kiểm soát quyền xem (công khai, riêng tư, cần mật mã), giới hạn sĩ số và cấu hình đề cương chi tiết.

#### B. Quản lý Học viên & Danh sách lớp học
- **Quản lý danh sách ghi danh:**
  - Thêm học viên thủ công bằng email hoặc mã định danh học viên.
  - Nhập/xuất danh sách học viên hàng loạt thông qua tệp mẫu Excel / CSV.
  - Tạo mã mời (join code) hoặc đường dẫn liên kết để học viên tự đăng ký vào lớp.
  - Phê duyệt hoặc từ chối các yêu cầu tham gia khóa học.
- **Phân nhóm học tập (Cohorts / Groups):** Chia lớp thành các nhóm thực hành, nhóm làm bài tập lớn; thiết lập bài tập nhóm và khu vực thảo luận riêng cho từng nhóm.
- **Hồ sơ tiến độ từng học viên:** Xem danh sách toàn bộ học viên kèm ảnh đại diện, ngày tham gia, lần cuối truy cập, tỉ lệ hoàn thành bài học và kết quả kiểm tra.

#### C. Thiết kế bài kiểm tra & Ngân hàng câu hỏi
- **Công cụ tạo bài thi trắc nghiệm linh hoạt:**
  - Soạn các dạng câu hỏi: Chọn một đáp án, chọn nhiều đáp án, Đúng/Sai, ghép nối, sắp xếp thứ tự, điền khuyết và câu hỏi tự luận.
  - Cấu hình bài thi: Giới hạn thời gian làm bài, số lần làm bài tối đa, điểm đạt yêu cầu, xáo trộn thứ tự câu hỏi và đảo thứ tự đáp án.
  - Quản lý chế độ xem đáp án: Hiện ngay sau khi nộp, chỉ hiện sau ngày kết thúc làm bài, hoặc ẩn hoàn toàn đáp án đúng.
- **Ngân hàng câu hỏi tập trung (Question Bank):**
  - Lưu trữ và phân loại câu hỏi theo chủ đề, chương học, mức độ nhận thức (Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao) và gắn thẻ tag.
  - Tạo đề thi ngẫu nhiên tự động: Rút ngẫu nhiên một số lượng câu hỏi từ ngân hàng theo ma trận đề (ví dụ: lấy ngẫu nhiên 15 câu từ Ngân hàng Chương 1 và 15 câu từ Chương 2).
- **Thiết kế bài tập tự luận/dự án:**
  - Thiết lập yêu cầu đề bài, tệp đính kèm, định dạng tệp cho phép nộp, thời hạn chót và quy định trừ điểm nộp trễ.
  - Xây dựng **Ma trận tiêu chí chấm điểm (Rubric)** tương tác với các mức điểm, mô tả chi tiết từng tiêu chí và trọng số rõ ràng.
  - Tùy chọn kiểm tra trùng lặp/đạo văn và giới hạn dung lượng tải lên.

#### D. Quy trình chấm điểm & Phản hồi bài nộp
- **Không gian chấm điểm tập trung (SpeedGrader):**
  - Giao diện chấm bài song song trực quan: Bài nộp của học viên hiển thị bên trái, bảng điểm và rubric chấm hiển thị bên phải.
  - Công cụ sửa bài & chú thích trực tiếp trên file PDF/tài liệu (highlight, gạch chân, ghi chú đính kèm, vẽ chú thích).
- **Chấm điểm theo Rubric một chạm:** Bấm chọn các mức đạt được trong rubric để hệ thống tự động cộng dọn điểm tổng, kèm ô nhận xét riêng cho từng tiêu chí.
- **Đa dạng hình thức phản hồi:** Nhập nhận xét bằng chữ, đính kèm tệp sửa lại, ghi âm lời dặn hoặc quay clip nhận xét ngắn.
- **Quản lý Sổ điểm lớp học tổng thể:**
  - Bảng ma trận điểm dạng bảng tính Excel trực quan.
  - Cấu hình trọng số điểm thành phần (ví dụ: Chuyên cần 10%, Bài tập 20%, Giữa kỳ 30%, Cuối kỳ 40%).
  - Công cụ điều chỉnh điểm: Cộng điểm khuyến khích, hạ chuẩn điểm, loại bỏ điểm thấp nhất, ẩn điểm tạm thời khi chưa chấm xong toàn bộ lớp.
  - Xuất bảng điểm lớp ra file Excel (XLSX) hoặc CSV phục vụ báo cáo.

#### E. Theo dõi tiến độ & Báo cáo phân tích học tập
- **Bảng điều khiển phân tích lớp học:** Thống kê trực quan tỉ lệ hoàn thành bài học trung bình, biểu đồ phân bố điểm số và mức độ chuyên cần của cả lớp.
- **Hệ thống cảnh báo học viên có nguy cơ (At-Risk Alerts):** Tự động phát hiện và thông báo danh sách học viên không đăng nhập nhiều ngày, chưa nộp bài tập hoặc điểm số dưới mức trung bình.
- **Nhật ký hoạt động chi tiết (Activity Logs):** Xem chi tiết từng học viên đã xem video bao nhiêu phút, đã truy cập những tài nguyên nào, lịch sử làm bài thi ra sao.
- **Phân tích chất lượng câu hỏi thi (Item Analysis):** Đo lường độ khó, độ phân biệt của từng câu hỏi trắc nghiệm, phát hiện những câu hỏi có tỷ lệ học viên làm sai bất thường để hiệu chỉnh giáo trình giảng dạy.

#### F. Tương tác lớp học & Giảng dạy trực tuyến
- **Phát thông báo lớp:** Soạn, lên lịch và gửi thông báo quan trọng đến toàn bộ lớp học kèm tùy chọn gửi tự động vào hộp thư email của học viên.
- **Điều hành diễn đàn thảo luận:** Ghim các câu hỏi/chủ đề trọng tâm lên đầu trang, đánh dấu câu trả lời hay của học viên, khóa các luồng thảo luận đã hoàn tất và kiểm duyệt nội dung.
- **Tổ chức buổi học trực tuyến & Giờ giải đáp:** Lên lịch họp qua Microsoft Teams / Zoom trực tiếp từ hệ thống; tự động ghi nhận danh sách điểm danh tham dự.
- **Gửi tin nhắn có mục tiêu:** Lọc và gửi thông báo/nhắc nhở nhanh tới một nhóm học viên cụ thể (ví dụ: gửi tin nhắn nhắc nhở riêng cho các bạn chưa nộp bài tập 1).

---

### 3.3. Phân hệ Quản trị viên (Administrator)

#### A. Quản lý Người dùng & Định danh
- Tìm kiếm, lọc và quản lý toàn bộ danh sách tài khoản học viên, giáo viên trong toàn trường/tổ chức.
- Phân bổ, điều chỉnh hoặc thu hồi vai trò người dùng (Học viên, Giáo viên, Trợ giảng, Trưởng bộ môn, Quản trị viên).
- Nhập/xuất danh sách tài khoản hàng loạt, khóa hoặc xóa tài khoản.
- Quản lý danh sách tên miền email được phép đăng nhập (Domain Allowlist) và cấu hình liên kết thư mục người dùng doanh nghiệp.

#### B. Giám sát & Quản trị Khóa học
- Tạo lập và phân cấp danh mục khoa, viện, bộ môn và chuyên ngành đào tạo.
- Kiểm duyệt, phê duyệt, lưu trữ hoặc chuyển giao quyền sở hữu khóa học giữa các giảng viên.
- Theo dõi tổng thể số lượng ghi danh, tải trọng môn học và sức chứa hệ thống.
#### C. Cấu hình Hệ thống & Tích hợp Mở rộng
- Thiết lập nhận diện thương hiệu: Tên trường/tổ chức, logo, biểu tượng favicon, mã màu giao diện và mẫu email hệ thống.
- Cấu hình các kết nối tích hợp: SSO (Microsoft Entra ID / Office 365, Google Workspace), dịch vụ email máy chủ SMTP, kho lưu trữ đám mây, các công cụ chuẩn LTI 1.3.
- Cấu hình quy tắc gửi email thông báo tự động.

#### D. An ninh, Nhật ký & Tuân thủ Dữ liệu
- Hệ thống ghi nhật ký hoạt động (Audit Logs) chi tiết: Theo dõi lịch sử thay đổi vai trò, sửa điểm, xóa nội dung, đăng nhập hệ thống.
- Tuân thủ quyền riêng tư dữ liệu: Hỗ trợ trích xuất dữ liệu người dùng, xử lý yêu cầu xóa tài khoản theo chuẩn GDPR.
- Cơ chế sao lưu và khôi phục dữ liệu (Backup & Restore), quản lý hạn ngạch dung lượng lưu trữ (Storage Quota) và giám sát hiệu năng máy chủ.

