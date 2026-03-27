from django import forms

class PlantForm(forms.Form):
    image = forms.ImageField(required=True)