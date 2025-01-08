from django_cron import CronJobBase, Schedule
from .management.commands.send_reminders import Command as SendRemindersCommand

class SendRemindersCronJob(CronJobBase):
    RUN_AT_TIMES = ['08:00']  # Default run time; adjust this as necessary.

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'mood.send_reminders_cron_job'  # A unique code for the job.

    def do(self):
        # Run the management command for sending reminders
        SendRemindersCommand().handle()
