from django.test import TestCase
from freezegun import freeze_time

from datetime import date

from qlab.apps.accounts.models import User
from qlab.apps.company.models import LabDevice


class LabDeviceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Foo')
        LabDevice.objects.create(
            user=self.user,
            name='Test Device',
            serial_number='Test serial number',
            start_date=date(2020, 5, 6),
            period=1,
        )
        return super().setUp()

    @freeze_time('2020-06-05')
    def test_lab_device_renew(self):
        lab_device = LabDevice.objects.first()
        lab_device.save()
        self.assertEqual(LabDevice.objects.count(), 2)
        self.assertEqual(
            LabDevice.objects.filter().last().start_date, date(2020, 5, 7)
        )
