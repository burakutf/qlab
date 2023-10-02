from django.conf import settings
from django.urls import reverse
from django.test import RequestFactory

from rest_framework.test import APITestCase

from qlab.apps.accounts.models import User
from qlab.api.auth.views import LoginView

class LoginWithEmailTestCase(APITestCase):
    def setUp(self):
        self.username = 'burak'
        self.password = '12345678'
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

    def test_login_with_valid(self):
        request = RequestFactory().post(
            '/api/',
            {
                'email': self.username,
                'password': self.password,
            },
        )
        response = LoginView().post(request, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_login_with_not_valid(self):
        request = RequestFactory().post(
            '/api/',
            {
                'email': self.email,
                'password': '1234567',
            },
        )
        response = LoginView().post(request, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0].code, 'authorization'
        )
