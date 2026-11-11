from django.db import models
from django.conf import settings


class CheckInRecord(models.Model):
    # Người dùng (nếu có đăng nhập, để null nếu check-in khách)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Người điểm danh",
    )
    # Tọa độ gửi từ thiết bị
    user_latitude = models.FloatField(verbose_name="Vĩ độ người dùng")
    user_longitude = models.FloatField(verbose_name="Kinh độ người dùng")
    accuracy_meters = models.FloatField(
        null=True, blank=True, verbose_name="Độ chính xác GPS (m)"
    )

    # Tọa độ sự kiện/phòng học mốc
    target_latitude = models.FloatField(verbose_name="Vĩ độ mục tiêu")
    target_longitude = models.FloatField(verbose_name="Kinh độ mục tiêu")

    # Kết quả tính toán
    distance_meters = models.FloatField(verbose_name="Khoảng cách thực tế (m)")
    allowed_radius_meters = models.FloatField(
        default=50.0, verbose_name="Bán kính cho phép (m)"
    )
    is_valid = models.BooleanField(
        default=False, verbose_name="Điểm danh hợp lệ"
    )
    message = models.CharField(
        max_length=255, blank=True, verbose_name="Thông báo kết quả"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Thời gian check-in"
    )

    class Meta:
        verbose_name = "Bản ghi điểm danh"
        verbose_name_plural = "Danh sách bản ghi điểm danh"
        ordering = ["-created_at"]

    def __str__(self):
        status = "Thành công" if self.is_valid else "Thất bại"
        user_name = self.user.username if self.user else "Ẩn danh"
        return f"[{status}] {user_name} - {self.distance_meters:.1f}m ({self.created_at.strftime('%H:%M %d/%m/%Y')})"