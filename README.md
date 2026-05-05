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

## Pi data ingestion

The dashboard now accepts direct telemetry writes from a Raspberry Pi through a JSON endpoint at `/api/flight-data/ingest/`.

Send `wind_speed`, `humidity`, `altitude`, and an optional ISO 8601 `timestamp`.

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/flight-data/ingest/ \
	-H "Content-Type: application/json" \
	-d '{"wind_speed": 6.4, "humidity": 52.1, "altitude": 84.0, "timestamp": "2026-05-05T12:30:00Z"}'
```

The dashboard polls `/api/flight-data/latest/` every few seconds so the latest values update without a manual refresh.

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

## Default login

For local development, the app creates a default admin account after migrations run:

- username: `admin`
- password: `admin`

Use this only for local testing.
