from django import forms
from django.utils.timezone import now
from datetime import timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Mood

def validate_date_within_two_weeks(value):
    """Validator to ensure the date is no more than 2 weeks before today."""
    if value < now().date() - timedelta(weeks=2):
        raise forms.ValidationError("You cannot add an entry with a date more than 2 weeks ago.")

class MoodEntryForm(forms.ModelForm):
    date = forms.DateField(
        initial=now().date,  # Prepopulate with today's date
        widget=forms.DateInput(attrs={"type": "date"}),
        validators=[validate_date_within_two_weeks],
    )

    class Meta:
        model = Mood
        fields = ["date", "mood_type", "note", "action"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
            "action": forms.Textarea(attrs={"rows": 3}),
        }
