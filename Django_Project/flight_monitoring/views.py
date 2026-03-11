from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FlightDataForm
from .models import FlightData


def flight_data_list(request):
	flight_data = FlightData.objects.all()
	chart_records = FlightData.objects.order_by("timestamp")
	chart_labels = [record.timestamp.strftime("%Y-%m-%d %H:%M:%S") for record in chart_records]
	wind_speed_data = [float(record.wind_speed) for record in chart_records]
	humidity_data = [float(record.humidity) for record in chart_records]

	return render(
		request,
		"flight_monitoring/flight_logs.html",
		{
			"flight_data": flight_data,
			"chart_labels": chart_labels,
			"wind_speed_data": wind_speed_data,
			"humidity_data": humidity_data,
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

	return render(
		request,
		"home.html",
		{
			"form": form,
			"latest_reading": latest_reading,
		},
	)
