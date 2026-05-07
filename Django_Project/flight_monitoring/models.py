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


class FlightSession(models.Model):
	started_at = models.DateTimeField(default=timezone.now, db_index=True)
	last_sample_at = models.DateTimeField(null=True, blank=True, db_index=True)
	ended_at = models.DateTimeField(null=True, blank=True, db_index=True)
	sample_count = models.PositiveIntegerField(default=0)
	log_text = models.TextField(blank=True)

	class Meta:
		ordering = ["-started_at"]

	def append_reading(self, reading):
		log_line = (
			f"{timezone.localtime(reading.timestamp):%Y-%m-%d %H:%M:%S} | "
			f"wind_speed={float(reading.wind_speed):.2f} m/s | "
			f"humidity={float(reading.humidity):.2f}% | "
			f"altitude={float(reading.altitude):.2f} m | "
			f"safety={reading.safety_rating}"
		)
		self.log_text = f"{self.log_text}\n{log_line}" if self.log_text else log_line
		self.last_sample_at = reading.timestamp
		self.sample_count += 1

	def close(self, timestamp=None):
		self.ended_at = timestamp or self.last_sample_at or timezone.now()

	def download_filename(self):
		return f"flight-log-{timezone.localtime(self.started_at):%Y%m%d-%H%M%S}.txt"

	def __str__(self):
		status = "active" if self.ended_at is None else "closed"
		return (
			f"Flight session starting at {self.started_at:%Y-%m-%d %H:%M:%S} | "
			f"{self.sample_count} samples | {status}"
		)
