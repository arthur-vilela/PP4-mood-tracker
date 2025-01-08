from django.urls import path
from .views import logout_confirm_view, ProfileUpdateView, CustomPasswordChangeView

app_name = "users"

urlpatterns = [
    path("logout/", logout_confirm_view, name="logout_confirm"),
    path("edit-profile/", ProfileUpdateView.as_view(), name="edit_profile"),
    path("change-password/", CustomPasswordChangeView.as_view(), name="change_password"),
]
