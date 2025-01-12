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
    """
    Renders the Logout Confirmation page.
    Allows the user to confirm and process the logout action.

    **Template:**
    :template:`account/logout_confirm.html`.
    """
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "account/logout_confirm.html")


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    """
    Renders the Profile Update page.
    Allows the user to update their username and email.

    **Context**
    ``form``
        Instance of :form:`users.ProfileUpdateForm`.

    **Template:**
    :template:`users/profile_update.html`.
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"
    success_url = "/dashboard/" 
    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    """
    Renders the Password Change page.
    Allows the user to securely update their password.

    **Context**
    ``form``
        Instance of :form:`users.StyledPasswordChangeForm`.

    **Template:**
    :template:`users/password_change.html`.
    """
    form_class = StyledPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("dashboard:dashboard_home") 