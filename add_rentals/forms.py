from django import forms
from .models import Rental, Reservation


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['name', 'description', 'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'number_of_beds', 'images', 'address_city', 'address_street']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'end_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
