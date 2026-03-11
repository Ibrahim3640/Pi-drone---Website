from collections import defaultdict

from django.utils import timezone


TIME_PERIODS = [
	("Night", 0, 6),
	("Morning", 6, 12),
	("Afternoon", 12, 18),
	("Evening", 18, 24),
]


def calculate_flight_safety_status(wind_speed, humidity, altitude):
	wind_speed = float(wind_speed)
	humidity = float(humidity)
	altitude = float(altitude)

	if wind_speed > 20 or humidity > 90 or altitude > 200:
		return "Dangerous"

	if wind_speed > 12 or humidity > 75 or altitude > 120:
		return "Caution"

	return "Safe"


def wind_speed_to_kmh(wind_speed):
	return round(float(wind_speed) * 3.6, 1)


def get_time_period(timestamp):
	local_timestamp = (
		timezone.localtime(timestamp) if timezone.is_aware(timestamp) else timestamp
	)
	hour = local_timestamp.hour

	for label, start_hour, end_hour in TIME_PERIODS:
		if start_hour <= hour < end_hour:
			return label

	return "Night"


def get_altitude_band(altitude):
	band = int(round(float(altitude) / 20.0) * 20)
	return max(20, band)


def build_conditions_summary(flight_data_records):
	grouped_data = {}

	for record in flight_data_records:
		altitude_band = get_altitude_band(record.altitude)
		time_period = get_time_period(record.timestamp)

		altitude_group = grouped_data.setdefault(
			altitude_band,
			{
				"altitude_label": f"{altitude_band}m",
				"total_readings": 0,
				"periods": defaultdict(
					lambda: {
						"wind_total": 0.0,
						"humidity_total": 0.0,
						"altitude_total": 0.0,
						"count": 0,
					}
				),
			},
		)

		period_group = altitude_group["periods"][time_period]
		period_group["wind_total"] += float(record.wind_speed)
		period_group["humidity_total"] += float(record.humidity)
		period_group["altitude_total"] += float(record.altitude)
		period_group["count"] += 1
		altitude_group["total_readings"] += 1

	summary_cards = []
	for altitude_band in sorted(grouped_data):
		altitude_group = grouped_data[altitude_band]
		period_summaries = []

		for label, _, _ in TIME_PERIODS:
			period_group = altitude_group["periods"].get(label)
			if not period_group:
				continue

			average_wind_speed = period_group["wind_total"] / period_group["count"]
			average_humidity = period_group["humidity_total"] / period_group["count"]
			average_altitude = period_group["altitude_total"] / period_group["count"]

			period_summaries.append(
				{
					"label": label,
					"sample_count": period_group["count"],
					"avg_wind_speed_mps": round(average_wind_speed, 1),
					"avg_wind_speed_kmh": wind_speed_to_kmh(average_wind_speed),
					"avg_humidity": round(average_humidity, 1),
					"safety_rating": calculate_flight_safety_status(
						average_wind_speed,
						average_humidity,
						average_altitude,
					),
				}
			)

		summary_cards.append(
			{
				"altitude_label": altitude_group["altitude_label"],
				"total_readings": altitude_group["total_readings"],
				"periods": period_summaries,
			}
		)

	return summary_cards