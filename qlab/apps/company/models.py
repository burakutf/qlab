from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from qlab.apps.accounts.models import User

from qlab.apps.core.utils.set_path import SetPathAndRename


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tax_number = models.CharField(max_length=10)
    authorized_person = models.CharField(max_length=50)
    contact_info = PhoneNumberField(null=True, blank=True, db_index=True)
    contact_info_mail = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    plate = models.CharField(max_length=16)
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    inspection_date = models.DateField(null=True, blank=True)
    insurance_date = models.DateField()
    maintenance_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.plate


class QualityMethod(models.Model):
    measurement_name = models.CharField(max_length=64)
    measurement_number = models.CharField(max_length=64)
    general_information = models.CharField(
        max_length=64, null=True, blank=True
    )
    price = models.IntegerField(default=0)
    general_file = models.FileField(
        upload_to=SetPathAndRename('method/'), null=True, blank=True
    )


class LabDevice(models.Model):
    user = models.OneToOneField(User, models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    serial_number = models.CharField(max_length=128)
    calibration_date = models.DateField()
    calibration_period = models.CharField(max_length=64)

    # TODO son calibration date ve period oluşturulcak period yaklaştıkça bildirim göndercem
