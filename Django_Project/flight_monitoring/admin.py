from django.contrib import admin

from .models import FlightData, FlightSession


@admin.register(FlightData)
class FlightDataAdmin(admin.ModelAdmin):
	list_display = ("timestamp", "wind_speed", "humidity", "altitude", "safety_rating")
	list_filter = ("safety_rating", "timestamp")
	ordering = ("-timestamp",)
	search_fields = ("timestamp",)


@admin.register(FlightSession)
class FlightSessionAdmin(admin.ModelAdmin):
	list_display = ("started_at", "ended_at", "sample_count")
	list_filter = ("started_at", "ended_at")
	ordering = ("-started_at",)
