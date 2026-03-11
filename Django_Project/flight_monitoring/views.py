from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FlightDataForm
from .models import FlightData
from .utils import build_conditions_summary, get_time_period, wind_speed_to_kmh


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
