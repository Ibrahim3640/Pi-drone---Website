from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("flight_monitoring.urls")),
    path("admin/", admin.site.urls),
]