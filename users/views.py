from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, 'users/landing_page.html')  # Replace with the actual template