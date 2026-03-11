# Drone Conditions Database
This repository contains a Django-based drone conditions database that allows the user to view the history of enviromental conditions within a specific area. Allows the user to notice patterns in the area so they are able to figure out when it will be safe to fly their drone.

## Project structure

- `Django_Project/pi_drone`: Django project configuration
- `Django_Project/flight_monitoring`: App for storing and displaying flight safety readings

## Stored telemetry data

The `FlightData` model stores:

- wind speed
- humidity
- altitude
- timestamp
- a calculated safety rating

## How the safety reading is predicted

Each submitted reading is checked against simple threshold rules:

- `Dangerous` if **any** of these are true:
	- wind speed > `20 m/s`
	- humidity > `90%`
	- altitude > `200 m`
- `Caution` if it is not Dangerous, but **any** of these are true:
	- wind speed > `12 m/s`
	- humidity > `75%`
	- altitude > `120 m`
- `Safe` if none of the above conditions are met.

So the app does not use machine learning; it uses clear rule-based comparisons to assign `Safe`, `Caution`, or `Dangerous`.

## Run locally

From `Django_Project`:

```bash
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py runserver
```

The home page provides a simple dashboard for entering readings and reviewing the latest 10 saved records. The Django admin also includes the flight readings model for management tasks.
