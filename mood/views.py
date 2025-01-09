from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from .forms import MoodEntryForm


@login_required
def mood_entry_view(request):
    if request.method == "POST":
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.save()
            messages.success(request, "Mood entry added successfully!")
            return redirect("dashboard:dashboard_home")  # Redirect to the dashboard after submission
        else:
            messages.error(request, "Error adding mood entry. Please check the form.")
    else:
        form = MoodEntryForm()
    return render(request, "mood/mood_entry.html", {"form": form})