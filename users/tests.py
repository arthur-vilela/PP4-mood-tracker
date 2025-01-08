from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()

class UsersViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="oldpassword"
        )
        self.client.login(username="testuser", password="oldpassword")

    def test_logout_confirm_view(self):
        """Test the logout confirmation view."""
        response = self.client.get(reverse("users:logout_confirm"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/logout_confirm.html")

        response = self.client.post(reverse("users:logout_confirm"))
        self.assertRedirects(response, "/")
        self.assertNotIn("_auth_user_id", self.client.session)  # Check if the user is logged out

    def test_profile_update_view_get(self):
        """Test GET request for profile update view."""
        response = self.client.get(reverse("users:edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_update.html")
        self.assertContains(response, "testuser")  # Prepopulated username
        self.assertContains(response, "testuser@example.com")  # Prepopulated email

    def test_profile_update_view_post(self):
        """Test POST request for profile update view."""
        response = self.client.post(reverse("users:edit_profile"), {
            "username": "updateduser",
            "email": "updateduser@example.com",
        })
        self.assertRedirects(response, "/dashboard/")

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_password_change_view_get(self):
        """Test GET request for password change view."""
        response = self.client.get(reverse("users:change_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/password_change.html")

    def test_password_change_view_post_success(self):
        """Test POST request for password change with valid data."""
        response = self.client.post(reverse("users:change_password"), {
            "old_password": "oldpassword",
            "new_password1": "newpassword123",
            "new_password2": "newpassword123",
        })
        self.assertRedirects(response, reverse("dashboard:dashboard_home"))

        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_password_change_view_post_failure(self):
        """Test POST request for password change with invalid data."""
        response = self.client.post(reverse("users:change_password"), {
            "old_password": "wrongpassword",
            "new_password1": "newpassword123",
            "new_password2": "newpassword123",
        })
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertContains(response, "Your old password was entered incorrectly.")  # Error message

        # Verify password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("oldpassword"))
