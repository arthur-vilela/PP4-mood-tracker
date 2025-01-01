from django.urls import path
from . import views

urlpatterns = [
    path('', views.mood_home, name='mood_home'),  # Placeholder view for now
]
