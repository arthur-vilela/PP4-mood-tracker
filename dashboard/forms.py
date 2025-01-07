from django import forms
from mood.models import Mood

class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ["date", "mood_type", "note", "action"]
