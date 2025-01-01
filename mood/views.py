from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def mood_home(request):
    return HttpResponse("Welcome to the Mood Tracker!")  # Temporary response for testing