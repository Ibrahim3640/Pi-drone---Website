import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import FlightDataForm
from .models import FlightData
from .utils import build_conditions_summary, get_time_period, wind_speed_to_kmh


def _serialize_flight_data(record):
	if not record:
		return None

	return {
		"id": record.id,
		"wind_speed": float(record.wind_speed),
		"wind_speed_kmh": wind_speed_to_kmh(record.wind_speed),
		"humidity": float(record.humidity),
		"altitude": float(record.altitude),
		"timestamp": timezone.localtime(record.timestamp).isoformat(),
		"timestamp_display": timezone.localtime(record.timestamp).strftime("%d %b %Y %H:%M"),
		"safety_rating": record.safety_rating,
	}


def _parse_timestamp(raw_timestamp):
	if not raw_timestamp:
		return timezone.now()

	parsed_timestamp = parse_datetime(str(raw_timestamp))
	if parsed_timestamp is None:
		raise ValueError("Invalid timestamp format.")

	if timezone.is_naive(parsed_timestamp):
		parsed_timestamp = timezone.make_aware(parsed_timestamp, timezone.get_current_timezone())

	return parsed_timestamp


def _get_request_payload(request):
	if request.content_type and request.content_type.startswith("application/json"):
		return json.loads(request.body.decode("utf-8") or "{}")

	return request.POST


@login_required
@require_GET
def latest_flight_data_api(request):
	latest_reading = FlightData.objects.first()
	return JsonResponse({"latest_reading": _serialize_flight_data(latest_reading)})


@csrf_exempt
@require_POST
def ingest_flight_data(request):
	try:
		payload = _get_request_payload(request)
		wind_speed = payload.get("wind_speed")
		humidity = payload.get("humidity")
		altitude = payload.get("altitude")
		timestamp = _parse_timestamp(payload.get("timestamp"))
		reading = FlightData.objects.create(
			wind_speed=wind_speed,
			humidity=humidity,
			altitude=altitude,
			timestamp=timestamp,
		)
	except (TypeError, ValueError, json.JSONDecodeError) as exc:
		return JsonResponse({"detail": str(exc)}, status=400)

	return JsonResponse({"latest_reading": _serialize_flight_data(reading)}, status=201)


def flight_data_list(request):
	flight_data = list(FlightData.objects.all())
	for record in flight_data:
		record.time_period_label = get_time_period(record.timestamp)
		record.wind_speed_kmh = wind_speed_to_kmh(record.wind_speed)

	conditions_summary = build_conditions_summary(flight_data)

	return render(
		request,
		"flight_monitoring/flight_logs.html",
		{
			"flight_data": flight_data,
			"conditions_summary": conditions_summary,
		},
	)


@login_required
def dashboard(request):
	if request.method == "POST":
		form = FlightDataForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("flight_monitoring:dashboard")
	else:
		form = FlightDataForm()

	latest_reading = FlightData.objects.first()
	if latest_reading:
		latest_reading.wind_speed_kmh = wind_speed_to_kmh(latest_reading.wind_speed)

	return render(
		request,
		"flight_monitoring/home.html",
		{
			"form": form,
			"latest_reading": latest_reading,
		},
	)
