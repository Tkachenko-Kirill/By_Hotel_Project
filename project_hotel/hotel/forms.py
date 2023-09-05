from django.forms import ModelForm, ValidationError
from django import forms
from datetime import date
from .models import Reservation

class SearchForm(forms.Form):
    date_in = forms.DateField(initial=date.today)
    date_out = forms.DateField(initial=date.today)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_name', 'check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput,
            'check_out_date': forms.DateInput,
        }
        initial = {
            'check_in_date': date.today(),
            'check_out_date': date.today(),
        }
