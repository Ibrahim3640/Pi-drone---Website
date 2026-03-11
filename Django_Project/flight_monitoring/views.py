from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FlightDataForm
from .models import FlightData


def flight_data_list(request):
	flight_data = FlightData.objects.all()

	return render(
		request,
		"flight_monitoring/flight_logs.html",
		{
			"flight_data": flight_data,
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
		"flight_monitoring/home.html",
		{
			"form": form,
			"latest_reading": latest_reading,
		},
	)
