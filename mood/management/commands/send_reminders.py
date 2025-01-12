import os
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from mood.models import NotificationSettings

class Command(BaseCommand):
    help = "Send daily reminder emails to users with notifications enabled"

    def handle(self, *args, **kwargs):
        users = NotificationSettings.objects.filter(notify_by_email=True)
        homepage_url = "https://pp4-mood-tracker-20082cf10f44.herokuapp.com/"

        for user_settings in users:
            user = user_settings.user
            try:
                # Create personalized email content
                subject = "Mood Tracker Daily Reminder"
                plain_message = (
                    "Hi there!\n\n"
                    "This is your daily reminder to log your mood in the Mood Tracker app!\n"
                    f"Click here to visit the app: {homepage_url}\n\n"
                    "Stay consistent, and have a great day!"
                )
                html_message = render_to_string("emails/daily_reminder.html", {
                    "user": user,
                    "homepage_url": homepage_url,
                })

                # Send email
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=os.getenv("EMAIL_USER"),
                    recipient_list=[user.email],
                    fail_silently=False,
                    html_message=html_message,  # Include the HTML message
                )
                self.stdout.write(f"Email sent to {user.email}")
            except Exception as e:
                self.stderr.write(f"Failed to send email to {user.email}: {e}")
