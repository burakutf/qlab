from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from qlab.apps.accounts.permissions import PermissionChoice

from qlab.apps.company.models import Company, Vehicle
from qlab.apps.core.models import ChoiceArrayField
from qlab.apps.core.utils.set_path import SetPathAndRename
from qlab.apps.tenant.models import Organization


class Role(models.Model):
    name = models.CharField(max_length=32)
    permissions = ChoiceArrayField(
        models.CharField(max_length=32, choices=PermissionChoice.choices),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        unique_together = ('name',)


class User(AbstractUser):
    class Genders(models.TextChoices):
        MAN = 'MN', 'Erkek'
        WOMAN = 'WMN', 'Kadın'

    organization = models.ForeignKey(Organization, models.CASCADE, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True, db_index=True)

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=3, choices=Genders.choices, null=True, blank=True
    )
    vehicle = models.ForeignKey(
        Vehicle, models.SET_NULL, 'user', null=True, blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name='roles',
        null=True,
        blank=True,
    )
    permissions = ChoiceArrayField(
        models.CharField(max_length=32, choices=PermissionChoice.choices),
        blank=True,
        default=list,
    )
    company = models.ForeignKey(
        Company, models.SET_NULL, 'user', null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.get_full_name() or str(self.id)


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    detail = models.CharField(max_length=256, null=True, blank=True)
    criminal_record = models.FileField(
        upload_to=SetPathAndRename('profile/criminal_record/'),
        null=True,
        blank=True,
    )
    military_certificate = models.FileField(
        upload_to=SetPathAndRename('profile/military_document/'),
        null=True,
        blank=True,
    )
    blood_group_certificate = models.FileField(
        upload_to=SetPathAndRename('profile/blood_group/'),
        null=True,
        blank=True,
    )
    driver_certificate = models.FileField(
        upload_to=SetPathAndRename('profile/driver_certificate/'),
        null=True,
        blank=True,
    )
    emission_certificate = models.FileField(
        upload_to=SetPathAndRename('profile/emission_certificate/'),
        null=True,
        blank=True,
    )
    height_certificate = models.FileField(
        upload_to=SetPathAndRename('profile/height_certificate/'),
        null=True,
        blank=True,
        help_text='Yüksekte çalışma belgesi',
    )
    graduate_certificate = models.FileField(
        upload_to=SetPathAndRename('profile/graduate_certificate/'),
        null=True,
        blank=True,
    )
