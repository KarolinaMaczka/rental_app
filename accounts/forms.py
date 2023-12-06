from django import forms
from .models import PersonalData


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = ['first_name', 'surname', 'address', 'phone_number']
