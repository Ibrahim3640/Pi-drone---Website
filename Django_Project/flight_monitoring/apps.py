from django.apps import AppConfig


class FlightMonitoringConfig(AppConfig):
    name = "flight_monitoring"

    def ready(self):
        from . import signals  # noqa: F401
