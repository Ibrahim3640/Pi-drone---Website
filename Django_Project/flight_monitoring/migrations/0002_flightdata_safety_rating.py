from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		("flight_monitoring", "0001_initial"),
	]

	operations = [
		migrations.RenameModel(
			old_name="FlightReading",
			new_name="FlightData",
		),
		migrations.AddField(
			model_name="flightdata",
			name="safety_rating",
			field=models.CharField(
				choices=[
					("Safe", "Safe"),
					("Caution", "Caution"),
					("Dangerous", "Dangerous"),
				],
				default="Safe",
				editable=False,
				max_length=10,
			),
		),
	]