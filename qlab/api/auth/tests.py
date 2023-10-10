from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class LoginWithEmailTestCase(APITestCase):
    def setUp(self):
        self.username = 'burak'
        self.password = '12345678'
        User = get_user_model()
        User.objects.create(username=self.username, password=self.password)

    def test_login_with_valid(self):
        url = reverse('api:login')
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_login_with_not_valid(self):
        url = reverse('api:login')
        data = {
            'username': self.username,
            'password': '1234567',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0].code, 'authorization'
        )
