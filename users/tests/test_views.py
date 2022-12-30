from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile
from users.forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')
        self.create_company_url = reverse('create-company')
        self.login_company_url = reverse('login-company')


    def test_UserRegisterView(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_post_UserRegisterView(self):
        pass

    def test_CreateCompanyView(self):
        response = self.client.get(self.create_company_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create-company.html')

    def test_LoginCompanyView(self):
        response = self.client.get(self.login_company_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login-company.html')

    def test_profileView(self):
        response = self.client.get(self.profile_url, {'user_info':user_info})
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'users/profile.html')