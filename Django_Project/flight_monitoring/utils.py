def calculate_flight_safety_status(wind_speed, humidity):
	wind_speed = float(wind_speed)
	humidity = float(humidity)

	if wind_speed > 20 or humidity > 90:
		return "Dangerous"

	if wind_speed > 12 or humidity > 75:
		return "Caution"

	return "Safe"