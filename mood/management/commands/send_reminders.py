from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mood.models import NotificationSettings

class Command(BaseCommand):
    help = "Send daily reminder emails to users with notifications enabled"

    def handle(self, *args, **kwargs):
        users = NotificationSettings.objects.filter(notify_by_email=True)
        for user_settings in users:
            user = user_settings.user
            send_mail(
                subject="Mood Tracker Reminder",
                message="This is your daily reminder to log your mood in the Mood Tracker app!",
                from_email=os.getenv("EMAIL_USER"),
                recipient_list=[user.email],
                fail_silently=False,
            )
        self.stdout.write(f"Sent reminders to {users.count()} users.")
