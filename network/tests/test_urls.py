from django.test import TestCase
from django.urls import reverse, resolve
from network.views import login_view, logout_view, register

# Create your tests here.

class UrlTestCase(TestCase):

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, login_view)
    
    def test_logout(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, logout_view)
    
    def test_register(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, register)
    