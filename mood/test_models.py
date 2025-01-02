from django.test import TestCase
from django.contrib.auth.models import User
from mood.models import Mood, NotificationSettings, UserPreferences
from datetime import time

# Create your tests here.

class MoodModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
    
    def test_mood_creation(self):
        mood = Mood.objects.create(
            user=self.user,
            mood_type="Happy",
            note="Feeling great!",
            action="Went for a run",
        )
        self.assertEqual(mood.user.username, "testuser")
        self.assertEqual(mood.mood_type, "Happy")
        self.assertIsNotNone(mood.created_at)
        self.assertIsNotNone(mood.updated_at)

    def test_string_representation(self):
        mood = Mood.objects.create(
            user=self.user,
            mood_type="Sad",
            note="Feeling down.",
        )
        self.assertEqual(str(mood), f"testuser - Sad on {mood.date}")


class NotificationSettingsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
    
    def test_notification_settings_creation(self):
        settings = NotificationSettings.objects.create(
            user=self.user,
            notify_by_email=True,
            notify_time=time(9, 0),
        )
        self.assertEqual(settings.user.username, "testuser")
        self.assertTrue(settings.notify_by_email)
        self.assertEqual(settings.notify_time, time(9, 0))

    def test_string_representation(self):
        settings = NotificationSettings.objects.create(
            user=self.user,
            notify_by_email=False,
        )
        self.assertEqual(str(settings), "testuser - Notifications disabled")


class UserPreferencesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
    
    def test_user_preferences_creation(self):
        preferences = UserPreferences.objects.create(
            user=self.user,
            dark_mode_enabled=True,
        )
        self.assertEqual(preferences.user.username, "testuser")
        self.assertTrue(preferences.dark_mode_enabled)

    def test_string_representation(self):
        preferences = UserPreferences.objects.create(
            user=self.user,
            dark_mode_enabled=False,
        )
        self.assertEqual(str(preferences), "testuser - Dark Mode disabled")
