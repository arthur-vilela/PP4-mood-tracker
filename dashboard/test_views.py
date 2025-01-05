from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from mood.models import Mood

class MoodChartViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com"
        )
        self.client.login(username="testuser", password="password123")

        # Create Mood entries with explicit dates
        Mood.objects.create(user=self.user, mood_type="Happy", date="2025-01-01")
        Mood.objects.create(user=self.user, mood_type="Sad", date="2025-01-02")

    def test_mood_chart_view_returns_json(self):
        response = self.client.get(reverse("dashboard:mood_chart"))
        self.assertEqual(response.status_code, 200)

        # Verify the JSON response
        mood_data = response.json()
        self.assertEqual(mood_data["labels"], ["2025-01-01", "2025-01-02"])
        self.assertEqual(mood_data["data"], ["Happy", "Sad"])
