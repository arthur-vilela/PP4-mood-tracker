import os
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta
from collections import Counter
from mood.models import Mood
from mood.models import NotificationSettings
from mood.models import UserPreferences
from mood.management.commands.send_reminders import Command as SendRemindersCommand
from .forms import MoodForm
import calendar


# Create your views here.
@login_required
def dashboard_view(request):
    """
    Renders the Dashboard page.
    Displays all mood entries for the logged-in user and provides a monthly breakdown of entries.
    
    **Context**
    ``moods``
        Queryset of all mood entries for the logged-in user, ordered by the most recent date.
    ``months``
        List of unique months with mood entries.

    **Template:**
    :template:`dashboard/dashboard.html`.
    """
    # Get all moods for the logged-in user
    moods = Mood.objects.filter(user=request.user).select_related('user').order_by('-date')

    # Generate a list of unique months with mood entries
    if moods.exists():
        start_date = moods.last().date  # Earliest mood date
        end_date = moods.first().date  # Latest mood date
        months = [
            start_date + timedelta(days=i * 30)
            for i in range((end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1)
        ]
    else:
        months = []

    dark_theme = request.session.get('dark_theme', False)
    
    return render(request, "dashboard/dashboard.html", {"moods": moods, "months": months, "dark_theme": dark_theme,})

@login_required
def mood_calendar_view(request):
    """
    Generates and returns JSON data for the Mood Calendar.
    The calendar is dynamically rendered using D3.js on the frontend.
    
    **Context**
    JSON response containing date-to-mood mapping, where each day is color-coded based on the most frequent mood type.

    **Template:**
    This view does not render a template. It returns a JSON response.
    """
    try:
        moods = Mood.objects.filter(user=request.user)
        mood_by_date = {}

        # Group moods by date
        for mood in moods:
            mood_by_date.setdefault(mood.date, []).append(mood.mood_type)

        # Determine the most common mood per date
        calendar_data = {
            date.strftime('%Y-%m-%d'): Counter(mood_types).most_common(1)[0][0]
            for date, mood_types in mood_by_date.items()
        }

        return JsonResponse(calendar_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def mood_history_view(request):
    """
    Renders the Mood History page.
    Allows users to view a chronological list of their mood entries.

    **Context**
    ``moods``
        Queryset of all mood entries for the logged-in user, ordered by the most recent date.

    **Template:**
    :template:`dashboard/mood_history.html`.
    """
    moods = Mood.objects.filter(user=request.user).select_related('user').order_by('-date')  # Fetch moods in descending order of date
    return render(request, 'dashboard/mood_history.html', {'moods': moods})


@login_required
def settings_view(request):
    """
    Renders the Settings page.
    Allows users to configure notification preferences and enable or disable dark mode.

    **Context**
    ``notification_settings``
        The notification settings for the logged-in user.
    ``preferences``
        The user preferences (e.g., dark mode) for the logged-in user.

    **Template:**
    :template:`dashboard/settings.html`.
    """
    try:
        notification_settings = NotificationSettings.objects.select_related('user').get(user=request.user)
    except NotificationSettings.DoesNotExist:
        notification_settings = NotificationSettings.objects.create(user=request.user)

    preferences, created = UserPreferences.objects.select_related('user').get_or_create(user=request.user)

    if request.method == "POST":
        notify_by_email = request.POST.get("notify_by_email", "off") == "on"
        dark_theme = request.POST.get("dark_theme", "off") == "on"

        # Save notification preferences
        notification_settings.notify_by_email = notify_by_email
        notification_settings.save()

        # Save dark theme preference
        preferences.dark_mode_enabled = dark_theme
        preferences.save()
        request.session["dark_theme"] = dark_theme

        messages.success(request, "Settings updated successfully.")
        return redirect("dashboard:settings")

    return render(request, "dashboard/settings.html", {
        "notification_settings": notification_settings,
        "preferences": preferences,
    })

@csrf_exempt
@require_POST
def trigger_send_reminders(request):
    """
    Trigger the Daily Reminder Email function.
    This view is designed for automation tools (e.g., Heroku Scheduler) to invoke the email reminder functionality.

    **Request Headers**
    ``X-SECRET-TOKEN``
        A secret token required to authenticate the request.

    **Response**
    - Success: JSON response with a success message.
    - Failure: JSON response with an error message and a 500 status code.

    **Template:**
    This view does not render a template. It returns a JSON response.
    """
    # Verify the request contains the secret token
    secret_token = request.headers.get("X-SECRET-TOKEN")
    expected_token = os.getenv("SECRET_TOKEN") 
    if secret_token != expected_token:
        return HttpResponseForbidden("Invalid secret token")

    # Trigger the send_reminders function
    try:
        send_reminders = SendRemindersCommand()
        send_reminders.handle()
        return JsonResponse({"status": "success", "message": "Reminders sent successfully"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def edit_mood_view(request, pk):
    """
    Renders the Edit Mood Entry page.
    Allows the user to update an existing mood entry.

    **Context**
    ``form``
        Instance of :form:`dashboard.MoodForm` pre-filled with the mood entry data.

    **Template:**
    :template:`dashboard/edit_mood.html`.
    """
    mood = get_object_or_404(Mood.objects.select_related('user'), pk=pk, user=request.user)
    if request.method == "POST":
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            messages.success(request, "Mood entry updated successfully!")
            return redirect("dashboard:mood_history")
        else:
            messages.error(request, "Error updating mood entry. Please check the form.")
    else:
        form = MoodForm(instance=mood)
    return render(request, "dashboard/edit_mood.html", {"form": form})


@login_required
def delete_mood_view(request, pk):
    """
    Handles deletion of a Mood Entry.
    Allows the user to delete a specific mood entry.

    **Context**
    No additional context is passed to the template.

    **Template:**
    This view does not render a template. It redirects to the Mood History page.
    """
    mood = get_object_or_404(Mood.objects.select_related('user'), pk=pk, user=request.user)
    mood.delete()
    messages.success(request, "Mood entry deleted successfully!")
    return redirect("dashboard:mood_history")