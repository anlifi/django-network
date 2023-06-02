from django.test import TestCase
from django.urls import reverse
from ..models import User

# Create your tests here.

class LoginViewTestCase(TestCase):

    def test_login_view(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        User.objects.create_user(username="testuser", password="12345")
        self.client.post(reverse("login"), {"username":"testuser", "password":"12345"})
        self.assertIn("_auth_user_id", self.client.session)

    def test_invalid_login(self):
        User.objects.create_user(username="testuser", password="12345")
        response = self.client.post(reverse("login"), {"username":"", "password":""}, follow=True)
        self.assertEqual(response.context["message"], "Invalid username and/or password.")
    

class LogoutViewTestCase(TestCase):

    def test_logout(self):
        User.objects.create_user(username="testuser", password="12345")
        self.client.post(reverse("login"), {"username":"testuser", "password":"12345"})
        self.assertIn("_auth_user_id", self.client.session)
        self.client.get("/logout")
        self.assertNotIn("_auth_user_id", self.client.session)
    

class RegisterTestCase(TestCase):

    def test_register_view(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        self.client.post(reverse("register"), {"username":"testuser", "email": "testuser@test.com", "password":"12345", "confirmation": "12345"})
        self.assertIn("_auth_user_id", self.client.session)

    def test_invalid_registration_passwords_mismatch(self):
        response = self.client.post(reverse("register"), {"username":"testuser", "email": "testuser@test.com", "password":"12345", "confirmation": "54321"}, follow=True)
        self.assertEqual(response.context["message"], "Passwords must match.")

    def test_invalid_registration_username_taken(self):
        User.objects.create_user(username="testuser", password="12345")
        response = self.client.post(reverse("register"), {"username":"testuser", "email": "testuser@test.com", "password":"12345", "confirmation": "12345"}, follow=True)
        self.assertEqual(response.context["message"], "Username already taken.")
