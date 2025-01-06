from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_home'),
    path("mood-chart/", views.mood_chart_view, name="mood_chart"),
    path('mood-history/', views.mood_history_view, name='mood_history'),
    path('notification-settings/', views.notification_settings_view, name='notification_settings'),
]