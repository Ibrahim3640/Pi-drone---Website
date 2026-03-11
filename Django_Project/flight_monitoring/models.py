from django.db import models
from django.utils import timezone


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
		wind_speed = float(self.wind_speed)
		humidity = float(self.humidity)
		altitude = float(self.altitude)

		if wind_speed > 20 or humidity > 90 or altitude > 200:
			return self.DANGEROUS
		if wind_speed > 12 or humidity > 75 or altitude > 120:
			return self.CAUTION
		return self.SAFE

	def save(self, *args, **kwargs):
		self.safety_rating = self.calculate_safety_rating()
		super().save(*args, **kwargs)

	def __str__(self):
		return (
			f"Flight data at {self.timestamp:%Y-%m-%d %H:%M:%S} | "
			f"Safety {self.safety_rating}"
		)
