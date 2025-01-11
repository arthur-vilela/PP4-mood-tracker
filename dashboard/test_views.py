from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from mood.models import NotificationSettings
from mood.models import Mood
from datetime import date

User = get_user_model()

class MoodChartViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.url = reverse("dashboard:mood_calendar")

    def test_mood_chart_view_returns_json(self):
        # Create sample mood entries for the user
        Mood.objects.create(user=self.user, date=date(2025, 1, 1), mood_type="Happy")
        Mood.objects.create(user=self.user, date=date(2025, 1, 2), mood_type="Sad")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        mood_data = response.json()
        self.assertEqual(mood_data.get("labels"), ["2025-01-01", "2025-01-02"])
        self.assertEqual(mood_data.get("data"), ["Happy", "Sad"])

    def test_mood_chart_view_with_no_moods(self):
        # Test the view when there are no mood entries
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        mood_data = response.json()
        self.assertEqual(mood_data["labels"], [])
        self.assertEqual(mood_data["data"], [])

    def test_mood_chart_view_with_unauthenticated_user(self):
        # Logout the authenticated user
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertIn("/accounts/login/", response.url)

    def test_mood_chart_view_with_invalid_mood_type(self):
        # Create a mood entry with a valid-length but invalid mood type
        invalid_mood = Mood.objects.create(user=self.user, date=date(2025, 1, 3), mood_type="Invalid")
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        mood_data = response.json()
        # Ensure the invalid mood type is still included in the response
        self.assertIn("Invalid", mood_data["data"])


class MoodHistoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        Mood.objects.create(user=self.user, date=date(2025, 1, 1), mood_type="Happy")
        Mood.objects.create(user=self.user, date=date(2025, 1, 2), mood_type="Sad")

    def test_mood_history_view_status_code(self):
        response = self.client.get(reverse('dashboard:mood_history'))
        self.assertEqual(response.status_code, 200)

    def test_mood_history_view_template(self):
        response = self.client.get(reverse('dashboard:mood_history'))
        self.assertTemplateUsed(response, 'dashboard/mood_history.html')

    def test_mood_history_view_content(self):
        Mood.objects.create(user=self.user, date="2025-01-01", mood_type="Happy")
        Mood.objects.create(user=self.user, date="2025-01-02", mood_type="Sad")
        response = self.client.get(reverse('dashboard:mood_history'))
        self.assertContains(response, "Happy")
        self.assertContains(response, "Sad")


class NotificationSettingsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.notification_settings_url = reverse("dashboard:settings")
        self.client.login(username="testuser", password="password")

    def test_notification_settings_view_status_code(self):
        response = self.client.get(self.notification_settings_url)
        self.assertEqual(response.status_code, 200)

    def test_notification_settings_view_template(self):
        response = self.client.get(self.notification_settings_url)
        self.assertTemplateUsed(response, "dashboard/settings.html")

    def test_notification_settings_update(self):
        response = self.client.post(self.notification_settings_url, {
            "notify_by_email": "on"  # Simulate enabling email notifications
        })
        self.assertRedirects(response, self.notification_settings_url)  # Check redirection after submission

        # Fetch updated settings from the database
        notification_settings = NotificationSettings.objects.get(user=self.user)
        self.assertTrue(notification_settings.notify_by_email)