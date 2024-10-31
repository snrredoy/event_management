from django import forms
from .models import Event, BookingEvent

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['category', 'name', 'description', 'date', 'location', 'capacity']

    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label= "Date and Time"
    )
    

