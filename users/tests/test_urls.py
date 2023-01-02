from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import UserRegisterView, profile
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):
    
    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, UserRegisterView)

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)
    
    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)