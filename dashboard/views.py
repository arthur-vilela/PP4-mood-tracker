from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def dashboard_home(request):
    return HttpResponse("Welcome to the Dashboard!")  # Temporary response for testing