from django import forms

from .models import FlightData


class FlightDataForm(forms.ModelForm):
    timestamp = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = FlightData
        fields = ["wind_speed", "humidity", "altitude", "timestamp"]
        widgets = {
            "wind_speed": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Wind speed (m/s)"}
            ),
            "humidity": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Humidity (%)"}
            ),
            "altitude": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Altitude (m)"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["timestamp"].widget.attrs.setdefault("placeholder", "Timestamp")