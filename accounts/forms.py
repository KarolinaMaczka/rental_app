from django import forms
from .models import PersonalData


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = [ 'address', 'phone_number']
