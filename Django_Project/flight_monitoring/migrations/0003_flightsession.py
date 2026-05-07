from datetime import timedelta

from django.db import migrations, models
from django.utils import timezone


SESSION_GAP = timedelta(seconds=15)


def build_log_line(reading):
    return (
        f"{reading.timestamp:%Y-%m-%d %H:%M:%S} | "
        f"wind_speed={float(reading.wind_speed):.2f} m/s | "
        f"humidity={float(reading.humidity):.2f}% | "
        f"altitude={float(reading.altitude):.2f} m | "
        f"safety={reading.safety_rating}"
    )


def forwards(apps, schema_editor):
    FlightData = apps.get_model("flight_monitoring", "FlightData")
    FlightSession = apps.get_model("flight_monitoring", "FlightSession")

    active_session = None
    readings = FlightData.objects.order_by("timestamp", "id")
    for reading in readings:
        if active_session is None:
            active_session = FlightSession.objects.create(
                started_at=reading.timestamp,
                last_sample_at=reading.timestamp,
            )
        else:
            gap = reading.timestamp - active_session.last_sample_at
            if gap > SESSION_GAP:
                active_session.ended_at = active_session.last_sample_at
                active_session.save(update_fields=["ended_at"])
                active_session = FlightSession.objects.create(
                    started_at=reading.timestamp,
                    last_sample_at=reading.timestamp,
                )

        log_line = build_log_line(reading)
        active_session.log_text = f"{active_session.log_text}\n{log_line}" if active_session.log_text else log_line
        active_session.last_sample_at = reading.timestamp
        active_session.sample_count += 1
        active_session.save(update_fields=["log_text", "last_sample_at", "sample_count"])

    if active_session is not None and active_session.ended_at is None:
        active_session.ended_at = active_session.last_sample_at
        active_session.save(update_fields=["ended_at"])


def backwards(apps, schema_editor):
    FlightSession = apps.get_model("flight_monitoring", "FlightSession")
    FlightSession.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("flight_monitoring", "0002_flightdata_safety_rating"),
    ]

    operations = [
        migrations.CreateModel(
            name="FlightSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(db_index=True, default=timezone.now),
                ),
                (
                    "last_sample_at",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "ended_at",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("sample_count", models.PositiveIntegerField(default=0)),
                ("log_text", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["-started_at"],
            },
        ),
        migrations.RunPython(forwards, backwards),
    ]
