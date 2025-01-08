from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import localtime, now
from mood.models import NotificationSettings
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Send daily email reminders to users to log their mood.'

    def handle(self, *args, **kwargs):
        current_time = localtime(now()).strftime("%H:%M")
        notifications = NotificationSettings.objects.filter(
            notify_by_email=True, 
            notify_time=current_time
        )

        for notification in notifications:
            user = notification.user
            if user.email:
                send_mail(
                    subject="Daily Mood Reminder",
                    message="Don't forget to log your mood today!",
                    from_email=os.getenv("EMAIL_USER"),
                    recipient_list=[user.email],
                )
                self.stdout.write(f"Email sent to {user.username} ({user.email})")

        self.stdout.write("Reminder emails processed.")
