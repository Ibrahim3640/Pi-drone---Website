from django.urls import path

from .views import dashboard, flight_data_list, ingest_flight_data, latest_flight_data_api

app_name = "flight_monitoring"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("flight-data/", flight_data_list, name="flight_data_list"),
    path("api/flight-data/latest/", latest_flight_data_api, name="flight_data_latest"),
    path("api/flight-data/ingest/", ingest_flight_data, name="flight_data_ingest"),
]