from django.contrib import admin

from .models import FlightData


@admin.register(FlightData)
class FlightDataAdmin(admin.ModelAdmin):
	list_display = ("timestamp", "wind_speed", "humidity", "altitude", "safety_rating")
	list_filter = ("safety_rating", "timestamp")
	ordering = ("-timestamp",)
	search_fields = ("timestamp",)
