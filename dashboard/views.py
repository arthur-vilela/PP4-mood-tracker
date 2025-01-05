from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mood.models import NotificationSettings
from mood.models import Mood

# Create your views here.
def dashboard_home(request):
    return HttpResponse("Welcome to the Dashboard!")  # Temporary response for testing


@login_required
def mood_chart_view(request):
    """View to generate data for mood charts."""
    moods = Mood.objects.filter(user=request.user).order_by('date')
    mood_data = {
        "labels": [mood.date.strftime('%Y-%m-%d') for mood in moods],
        "data": [mood.mood_type for mood in moods],
    }
    return JsonResponse(mood_data)


@login_required
def mood_history_view(request):
    """View to display the user's mood history."""
    moods = Mood.objects.filter(user=request.user).order_by('-date')  # Fetch moods in descending order of date
    return render(request, 'dashboard/mood_history.html', {'moods': moods})


@login_required
def notification_settings_view(request):
    """View to display and update notification settings."""
    try:
        notification_settings = NotificationSettings.objects.get(user=request.user)
    except NotificationSettings.DoesNotExist:
        notification_settings = NotificationSettings.objects.create(user=request.user)

    if request.method == "POST":
        notify_by_email = request.POST.get("notify_by_email", "off") == "on"
        notify_time = request.POST.get("notify_time")

        notification_settings.notify_by_email = notify_by_email
        notification_settings.notify_time = notify_time
        notification_settings.save()

        messages.success(request, "Notification settings updated successfully.")
        return redirect("dashboard:notification_settings")

    return render(request, "dashboard/notification_settings.html", {
        "notification_settings": notification_settings
    })