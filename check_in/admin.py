from django.contrib import admin
from django.utils.html import format_html
from .models import CheckInRecord


@admin.register(CheckInRecord)
class CheckInRecordAdmin(admin.ModelAdmin):
    # Các cột hiển thị trên danh sách bảng admin
    list_display = (
        "id",
        "display_user",
        "status_badge",
        "distance_meters",
        "allowed_radius_meters",
        "accuracy_meters",
        "created_at",
        "view_on_map",
    )

    # Bộ lọc nhanh ở thanh bên phải
    list_filter = ("is_valid", "created_at")

    # Thanh tìm kiếm theo tên tài khoản hoặc thông báo
    search_fields = ("user__username", "user__email", "message")

    # Các trường chỉ đọc (tránh việc sửa đổi dữ liệu log đã ghi)
    readonly_fields = (
        "user",
        "user_latitude",
        "user_longitude",
        "accuracy_meters",
        "target_latitude",
        "target_longitude",
        "distance_meters",
        "allowed_radius_meters",
        "is_valid",
        "message",
        "created_at",
    )

    # Số bản ghi trên mỗi trang
    list_per_page = 25

    # Phân nhóm giao diện khi xem chi tiết 1 bản ghi
    fieldsets = (
        (
            "Thông tin người dùng & Kết quả",
            {
                "fields": (
                    "user",
                    "is_valid",
                    "message",
                    "distance_meters",
                    "allowed_radius_meters",
                    "created_at",
                )
            },
        ),
        (
            "Dữ liệu Tọa độ & Độ chính xác",
            {
                "fields": (
                    "user_latitude",
                    "user_longitude",
                    "accuracy_meters",
                    "target_latitude",
                    "target_longitude",
                )
            },
        ),
    )

    # Hiển thị tên người dùng hoặc "Khách ẩn danh"
    @admin.display(description="Người điểm danh")
    def display_user(self, obj):
        return obj.user.username if obj.user else "Khách ẩn danh"

    # Hiển thị icon/màu sắc trực quan cho trạng thái
    @admin.display(description="Trạng thái", ordering="is_valid")
    def status_badge(self, obj):
        if obj.is_valid:
            return format_html(
                '<span style="color: white; background-color: #28a745; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Hợp lệ</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #dc3545; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Không hợp lệ</span>'
        )

    # Tạo đường link xem vị trí người dùng trên Google Maps
    @admin.display(description="Bản đồ")
    def view_on_map(self, obj):
        url = f"https://www.google.com/maps?q={obj.user_latitude:.6f},{obj.user_longitude:.6f}"
        return format_html(
            '<a href="{}" target="_blank" style="color: #007bff; text-decoration: underline;">Xem vị trí</a>',
            url,
        )