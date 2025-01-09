from mood.models import UserPreferences

class DarkModeMiddleware:
    """Middleware to ensure dark theme preference is set in the session."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            try:
                # Fetch or default to light theme
                preferences = UserPreferences.objects.get(user=request.user)
                request.session["dark_theme"] = preferences.dark_mode_enabled
            except UserPreferences.DoesNotExist:
                request.session["dark_theme"] = False  # Default to light mode
        else:
            # Ensure dark_theme key is cleared for unauthenticated users
            request.session.pop("dark_theme", None)

        response = self.get_response(request)
        return response
