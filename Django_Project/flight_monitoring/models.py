from django.db import models
from django.utils import timezone

from .utils import calculate_flight_safety_status


class FlightData(models.Model):
	SAFE = "Safe"
	CAUTION = "Caution"
	DANGEROUS = "Dangerous"

	SAFETY_STATUS_CHOICES = [
		(SAFE, "Safe"),
		(CAUTION, "Caution"),
		(DANGEROUS, "Dangerous"),
	]

	wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
	humidity = models.DecimalField(max_digits=5, decimal_places=2)
	altitude = models.DecimalField(max_digits=7, decimal_places=2)
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)
	safety_rating = models.CharField(
		max_length=10,
		choices=SAFETY_STATUS_CHOICES,
		default=SAFE,
		editable=False,
	)

	class Meta:
		ordering = ["-timestamp"]

	def calculate_safety_rating(self):
		return calculate_flight_safety_status(
			self.wind_speed,
			self.humidity,
			self.altitude,
		)

	def save(self, *args, **kwargs):
		self.safety_rating = self.calculate_safety_rating()
		super().save(*args, **kwargs)

	def __str__(self):
		return (
			f"Flight data at {self.timestamp:%Y-%m-%d %H:%M:%S} | "
			f"Safety {self.safety_rating}"
		)
