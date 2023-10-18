from django.test import TestCase

from qlab.apps.accounts.models import User
from qlab.apps.core.models import Notification

# Create your tests here.


class UserTest(TestCase):
    def test_create_user_notification(self):
        user = User.objects.create(
            username='Poo',
            email='burakucun@icloud.com',
            password='12345678',
            first_name='Ben',
            last_name='David',
        )
        notification = Notification.objects.filter(user=user).last()
        self.assertEqual(user.username, notification.user.username)
