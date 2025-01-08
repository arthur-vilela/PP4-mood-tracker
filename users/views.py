from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from .forms import ProfileUpdateForm
from .forms import StyledPasswordChangeForm

# Create your views here.

@login_required
def logout_confirm_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "account/logout_confirm.html")


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"
    success_url = "/dashboard/"  # Replace with your desired redirect URL

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    form_class = StyledPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("dashboard:dashboard_home")  # Adjust this to your dashboard's name