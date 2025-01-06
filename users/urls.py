from django.urls import path
from .views import logout_confirm_view

app_name = "users"

urlpatterns = [
    path("logout/", logout_confirm_view, name="logout_confirm"),
]
