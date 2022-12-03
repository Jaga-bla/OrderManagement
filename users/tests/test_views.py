from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile
from django.contrib.auth.models import User

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')


    def test_UserRegisterView(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_post_UserRegisterView(self):
        pass