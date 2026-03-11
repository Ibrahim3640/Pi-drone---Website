from django.urls import path

from .views import dashboard, flight_data_list

app_name = "flight_monitoring"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("flight-data/", flight_data_list, name="flight_data_list"),
]