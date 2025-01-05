from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
