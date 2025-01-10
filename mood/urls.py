from django.urls import path
from . import views

app_name = "mood"

urlpatterns = [
    path("entry/", views.mood_entry_view, name="mood_entry"),
]