from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

@login_required
def logout_confirm_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "account/logout_confirm.html")