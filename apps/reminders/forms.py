from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['reminder_type', 'reminder_time', 'repeat']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'repeat': forms.NumberInput(attrs={
                'placeholder': 'e.g. 7 for weekly',
                'min': 1
            }),
        }