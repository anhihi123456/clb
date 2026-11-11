import json
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .check_in_location import verify_check_in

# Tọa độ mốc cần điểm danh (VD: ĐHBK Hà Nội)
TARGET_LATITUDE = 21.004900
TARGET_LONGITUDE = 105.843300
MAX_RADIUS_METERS = 50.0


def check_in_page_view(request: HttpRequest):
    return render(request, "check_in/interface.html")


@csrf_exempt
@require_http_methods(["POST"])
def check_in_api_view(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8"))
        user_lat = float(payload.get("latitude"))
        user_lon = float(payload.get("longitude"))
        accuracy_raw = payload.get("accuracy")
        accuracy = float(accuracy_raw) if accuracy_raw is not None else None
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        return JsonResponse(
            {"success": False, "error": f"Tọa độ không hợp lệ: {str(e)}"}, 
            status=400
        )

    result = verify_check_in(
        user_latitude=user_lat,
        user_longitude=user_lon,
        target_latitude=TARGET_LATITUDE,
        target_longitude=TARGET_LONGITUDE,
        max_radius_meters=MAX_RADIUS_METERS,
        accuracy_meters=accuracy,
        allow_accuracy_buffer=True,
    )

    status_code = 200 if result.is_valid else 400
    return JsonResponse(result.to_dict(), status=status_code)