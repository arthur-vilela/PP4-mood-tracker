from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path("mood-chart/", views.mood_chart_view, name="mood_chart"),
    path('mood-history/', views.mood_history_view, name='mood_history'),
]