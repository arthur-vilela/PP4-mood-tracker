from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Create your models here.

class Mood(models.Model):
    class MoodChoices(models.TextChoices):
        HAPPY = "Happy", "Happy"
        SAD = "Sad", "Sad"
        ANXIOUS = "Anxious", "Anxious"
        ANGRY = "Angry", "Angry"
        EXCITED = "Excited", "Excited"
        CALM = "Calm", "Calm"
        TIRED = "Tired", "Tired"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood_type = models.CharField(
        max_length=10, 
        choices=MoodChoices.choices, 
        default=MoodChoices.CALM
    )
    note = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood_type} on {self.date}"


class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_settings")
    notify_by_email = models.BooleanField(default=True)
    notify_time = models.TimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Notifications {'enabled' if self.notify_by_email else 'disabled'}"


class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")
    dark_mode_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Dark Mode {'enabled' if self.dark_mode_enabled else 'disabled'}"
