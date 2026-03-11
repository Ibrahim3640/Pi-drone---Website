# Flight Saftey Monitor

This repository contains a Django-based drone flight safety monitoring system.

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

## Run locally

From `Django_Project`:

```bash
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py runserver
```

The home page provides a simple dashboard for entering readings and reviewing the latest 10 saved records. The Django admin also includes the flight readings model for management tasks.
