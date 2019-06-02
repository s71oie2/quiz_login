from django import forms
from .models import *

class PlantForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['exp']