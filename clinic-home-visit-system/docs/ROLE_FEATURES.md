# Phân Quyền và Tính Năng Theo Vai Trò (Role-Based Features)

Hệ thống Quản lý Phòng Khám và Đặt Lịch Khám Tại Nhà (Clinic Home Visit System) bao gồm 4 vai trò chính với các chức năng chuyên biệt:

---

## 1. Patient (Bệnh nhân / Người dùng)
Đây là vai trò mặc định của mọi người dùng khi đăng ký tài khoản.
- **Tìm kiếm Phòng khám:** Tìm kiếm theo tên, chuyên khoa, hoặc địa chỉ.
- **Lọc thông minh (GPS):** Tìm các phòng khám gần nhất dựa trên định vị, lọc theo bán kính hỗ trợ khám tại nhà.
- **Xem chi tiết:** Xem thông tin phòng khám, danh sách bác sĩ, bảng giá và các đánh giá từ người dùng khác.
- **Đặt lịch khám:** 
  - Đặt khám tại phòng khám.
  - Đặt khám tại nhà (Home Visit) kèm theo định vị địa chỉ khám.
- **Quản lý lịch hẹn:** Theo dõi trạng thái lịch khám (Pending, Confirmed, Completed, Cancelled).
- **Đánh giá & Phản hồi:** Gửi đánh giá (rating) và nhận xét (review) cho bác sĩ và phòng khám sau khi hoàn thành buổi khám.
- **Quản lý cá nhân:** Lưu địa chỉ mặc định, cập nhật hồ sơ cá nhân.

---

## 2. Doctor (Bác sĩ)
Bác sĩ tập trung vào việc quản lý các ca khám được phân công.
- **Dashboard bác sĩ:** Xem danh sách bệnh nhân đã đặt lịch trong ngày/tuần.
- **Quản lý trạng thái khám:** Cập nhật trạng thái lịch khám từ "Confirmed" → "In Progress" → "Completed".
- **Xem thông tin bệnh nhân:** Xem ghi chú của bệnh nhân, lý do khám và địa chỉ (nếu khám tại nhà).
- **Quản lý lịch biểu:** Xem lịch làm việc cá nhân được chủ phòng khám phân công.
- **Theo dõi phản hồi:** Xem các đánh giá và điểm xếp hạng từ bệnh nhân dành cho mình.

---

## 3. Clinic Owner (Chủ phòng khám)
Quản lý vận hành một hoặc nhiều phòng khám.
- **Quản lý Phòng khám:** Cập nhật thông tin phòng khám (giờ đóng/mở cửa, giá dịch vụ, chuyên khoa).
- **Quản lý Bác sĩ:** Thêm bác sĩ mới vào phòng khám, cập nhật thông tin và bằng cấp của bác sĩ.
- **Quản lý Lịch làm việc:** Thiết lập khung giờ làm việc cho từng bác sĩ theo các ngày trong tuần.
- **Giám sát đặt lịch:** Theo dõi toàn bộ lịch hẹn của tất cả bác sĩ trong phòng khám mình quản lý.
- **Quản lý Đánh giá:** Trả lời các nhận xét của khách hàng về phòng khám.
- **Thống kê:** Xem báo cáo về số lượng bệnh nhân, doanh thu và hiệu quả của từng bác sĩ.

---

## 4. Admin (Quản trị viên Hệ thống)
Người quản lý toàn bộ nền tảng.
- **Tổng quan Hệ thống:** Theo dõi các chỉ số đo lường toàn hệ thống (Tổng số user, phòng khám, số lượt đặt lịch thành công).
- **Quản lý Người dùng:** Kích hoạt/Khóa tài khoản người dùng, thay đổi vai trò (Role) của người dùng.
- **Quản lý Phòng khám & Bác sĩ:** Phê duyệt các phòng khám mới đăng ký, kiểm soát dữ liệu toàn sàn.
- **Quản trị Đánh giá:** Xử lý các báo cáo vi phạm liên quan đến đánh giá và bình luận.
- **Giám sát kỹ thuật:** Truy cập các bảng điều khiển (Grafana/Prometheus) để theo dõi hiệu năng hệ thống và lỗi logic.

---

## Bảng so sánh nhanh

| Tính năng | Patient | Doctor | Owner | Admin |
| :--- | :---: | :---: | :---: | :---: |
| Tìm kiếm & Đặt lịch | ✅ | ❌ | ❌ | ❌ |
| Đánh giá bác sĩ | ✅ | ❌ | ❌ | ❌ |
| Cập nhật trạng thái ca khám | ❌ | ✅ | ❌ | ❌ |
| Quản lý bác sĩ/schedules | ❌ | ❌ | ✅ | ✅ |
| Phê duyệt phòng khám | ❌ | ❌ | ❌ | ✅ |
| Quản lý toàn bộ User | ❌ | ❌ | ❌ | ✅ |
