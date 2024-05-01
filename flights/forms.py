from django import forms


class FlightSearchForm(forms.Form):
    origin = forms.CharField(required=True)
    destination = forms.CharField(required=True)
    departure_date = forms.DateField(required=True)
