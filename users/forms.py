from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

class StyledPasswordChangeForm(PasswordChangeForm):
    """Crispy-styled password change form."""
    pass

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]