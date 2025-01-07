from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_home'),
    path("mood-calendar/", views.mood_calendar_view, name="mood_calendar"),
    path('mood-history/', views.mood_history_view, name='mood_history'),
    path("edit-mood/<int:pk>/", views.edit_mood_view, name="edit_mood"),
    path("delete-mood/<int:pk>/", views.delete_mood_view, name="delete_mood"),
    path('settings/', views.settings_view, name='settings'),
]