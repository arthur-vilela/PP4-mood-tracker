from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from collections import Counter
from mood.models import NotificationSettings
from mood.models import Mood
from .forms import MoodForm
import calendar


# Create your views here.
@login_required
def dashboard_view(request):
    # Get all moods for the logged-in user
    moods = Mood.objects.filter(user=request.user).order_by('-date')

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

    return render(request, "dashboard/dashboard.html", {"moods": moods, "months": months})

@login_required
def mood_calendar_view(request):
    """View to generate data for mood calendar."""
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

@login_required
def mood_history_view(request):
    """View to display the user's mood history."""
    moods = Mood.objects.filter(user=request.user).order_by('-date')  # Fetch moods in descending order of date
    print("Debug: Moods QuerySet:", moods)  # Log the queryset
    return render(request, 'dashboard/mood_history.html', {'moods': moods})


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mood.models import NotificationSettings

@login_required
def settings_view(request):
    """View to manage user settings."""
    try:
        notification_settings = NotificationSettings.objects.get(user=request.user)
    except NotificationSettings.DoesNotExist:
        notification_settings = NotificationSettings.objects.create(user=request.user)

    if request.method == "POST":
        notify_by_email = request.POST.get("notify_by_email", "off") == "on"
        notify_time = request.POST.get("notify_time")
        dark_theme = request.POST.get("dark_theme", "off") == "on"

        # Validate time if email notifications are enabled
        if notify_by_email and not notify_time:
            messages.error(request, "Please provide a valid notification time.")
        else:
            notification_settings.notify_by_email = notify_by_email
            notification_settings.notify_time = notify_time if notify_time else None
            notification_settings.save()

            # Save dark theme preference in session
            request.session["dark_theme"] = dark_theme
            messages.success(request, "Settings updated successfully.")
            return redirect("dashboard:settings")

    return render(request, "dashboard/settings.html", {
        "notification_settings": notification_settings
    })




@login_required
def edit_mood_view(request, pk):
    mood = get_object_or_404(Mood, pk=pk, user=request.user)
    if request.method == "POST":
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            messages.success(request, "Mood entry updated successfully.")
            return redirect("dashboard:mood_history")
    else:
        form = MoodForm(instance=mood)
    return render(request, "dashboard/edit_mood.html", {"form": form})
    


@login_required
def delete_mood_view(request, pk):
    mood = get_object_or_404(Mood, pk=pk, user=request.user)
    mood.delete()
    messages.success(request, "Mood entry deleted successfully.")
    return redirect("dashboard:mood_history")