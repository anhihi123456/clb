from django.urls import path
from .views import check_in_page_view, check_in_api_view

urlpatterns = [
    path("", check_in_page_view, name="check_in_page"),
    path("api/", check_in_api_view, name="check_in_api"),
]