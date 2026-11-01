import os
import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now
from mood.models import Mood, NotificationSettings, UserPreferences

DEMO_USERNAME = "demo"
DEMO_EMAIL = "demo@example.com"

# (mood type, note, action) used to fill the demo account
SAMPLE_ENTRIES = [
    ("Happy", "Had lunch with old friends.", "Planned another meetup for next month."),
    ("Happy", "Finished a project I was proud of.", "Treated myself to a nice dinner."),
    ("Excited", "Booked a weekend trip to the mountains.", "Started a packing list."),
    ("Excited", "Got good news about a job application.", "Called my family to share it."),
    ("Calm", "Slow Sunday morning with coffee and a book.", "Kept my phone away until noon."),
    ("Calm", "Went for a long walk by the river.", "Want to make it a weekly habit."),
    ("Tired", "Slept badly and had a long day.", "Went to bed early."),
    ("Tired", "Too many meetings today.", "Blocked focus time in my calendar for tomorrow."),
    ("Anxious", "Presentation tomorrow and I don't feel ready.", "Rehearsed it twice and made notes."),
    ("Anxious", "Unexpected bills this month.", "Wrote down a budget for the next weeks."),
    ("Sad", "Missing home today.", "Video call with my parents."),
    ("Angry", "Stuck in traffic for an hour.", "Listened to a podcast to calm down."),
]


class Command(BaseCommand):
    help = "Create (or reset) a demo account with sample mood entries"

    def handle(self, *args, **kwargs):
        password = os.getenv("DEMO_PASSWORD")
        if not password:
            self.stdout.write("DEMO_PASSWORD is not set, skipping demo account")
            return

        # Start from a clean account every time, even if a visitor
        # changed the demo username or email
        User = get_user_model()
        User.objects.filter(Q(username=DEMO_USERNAME) | Q(email=DEMO_EMAIL)).delete()
        user = User.objects.create_user(
            username=DEMO_USERNAME, email=DEMO_EMAIL, password=password
        )
        NotificationSettings.objects.create(user=user, notify_by_email=False)
        UserPreferences.objects.create(user=user)

        # Fixed seed so the demo looks the same after every reset
        rng = random.Random(4)
        today = now().date()
        entries = 0
        for days_ago in range(60):
            # Skip some days, like a real user would
            if rng.random() < 0.2:
                continue
            mood_type, note, action = rng.choice(SAMPLE_ENTRIES)
            Mood.objects.create(
                user=user,
                date=today - timedelta(days=days_ago),
                mood_type=mood_type,
                note=note,
                action=action,
            )
            entries += 1

        self.stdout.write(f"Demo account '{DEMO_USERNAME}' ready with {entries} mood entries")
