from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _


from phonenumber_field.modelfields import PhoneNumberField

from qlab.apps.company.models import Company, Vehicle


class User(AbstractUser):
    class Genders(models.TextChoices):
        MAN = 'MN', 'Erkek'
        WOMAN = 'WMN', 'Kadın'

    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True, db_index=True)
    is_staff = models.BooleanField('is staff', default=False)

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=3, choices=Genders.choices, null=True, blank=True
    )
    vehicle = models.OneToOneField(
        Vehicle, models.SET_NULL, null=True, blank=True
    )
    company = models.ForeignKey(
        Company, models.SET_NULL, 'user', null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.get_full_name() or str(self.id)
