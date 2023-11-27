import re
from django.db import models
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField

from qlab.apps.core.utils.set_path import SetPathAndRename


class ProposalChoices(models.IntegerChoices):
    SENDING = 0, ('Teklif Gönderildi')
    APPROVAL = 1, ('Teklif Onaylandı')
    REJECT = 2, ('Teklif Kabul Edilmedi')
    WORKORDER = 3, ('İş Emri Oluşturuldu')


def validate_iban(value):
    if value:
        if not re.match(r'^[A-Z]{2}\d+$', value):
            raise ValidationError(
                'IBAN must start with two letters followed by digits.'
            )


class OrganizationInformation(models.Model):
    user = models.OneToOneField('accounts.User', models.PROTECT, null=True)
    owner = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phone = PhoneNumberField()
    mail = models.EmailField()
    signature = models.ImageField(
        upload_to=SetPathAndRename('signature/'), null=True, blank=True
    )
    title = models.CharField(max_length=128)
    bank_name = models.CharField(max_length=128, null=True)
    bank_no = models.CharField(max_length=128, null=True)
    bank_branch = models.CharField(max_length=128, null=True)
    bank_iban = models.CharField(
        max_length=128,
        null=True,
        validators=[validate_iban],
    )
    left_logo = models.ImageField(
        upload_to=SetPathAndRename('organization/logo/'),
        blank=True,
        null=True,
    )
    right_logo = models.ImageField(
        upload_to=SetPathAndRename('organization/logo/'),
        blank=True,
        null=True,
    )


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tax_number = models.CharField(max_length=10, null=True, blank=True)
    authorized_person = models.CharField(max_length=50)
    advisor = models.CharField(max_length=100, null=True, blank=True)
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


class LabDevice(models.Model):
    user = models.ForeignKey('accounts.User', models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    serial_number = models.CharField(max_length=128)
    start_date = models.DateField(help_text='calibration date', null=True)
    finish_date = models.DateField(null=True, blank=True)
    period = models.IntegerField(help_text='calibration period', null=True)


# TODO general_file silip düzenlenebilinir olması gerekiyor
class QualityMethod(models.Model):
    measurement_name = models.CharField(max_length=128)
    measurement_number = models.CharField(max_length=256)
    acceptance_date = models.DateField(null=True)
    general_file = models.FileField(
        upload_to=SetPathAndRename('method/'), null=True, blank=True
    )


class MethodParameters(models.Model):
    name = models.CharField(max_length=256)
    method = models.ManyToManyField(QualityMethod, related_name='parameters')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class ProposalDraft(models.Model):
    title = models.CharField(max_length=128)
    preface = models.TextField()
    terms = models.TextField()


class Proposal(models.Model):
    user = models.ForeignKey('accounts.User', models.PROTECT, null=True)
    company = models.ForeignKey(Company, models.PROTECT, null=True)
    draft = models.ForeignKey(ProposalDraft, models.SET_NULL, null=True)
    status = models.IntegerField(
        choices=ProposalChoices.choices, default=ProposalChoices.SENDING
    )
    file = models.FileField(null=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProposalMethodParameters(models.Model):
    proposal = models.ForeignKey(Proposal, models.CASCADE, 'parameters')
    parameter = models.ForeignKey(MethodParameters, on_delete=models.CASCADE)
    count = models.SmallIntegerField()
    methods = models.JSONField(null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )


class CompanyNote(models.Model):
    notes = models.TextField(null=True)
    date = models.DateField()


class WorkOrder(models.Model):
    proposal = models.ForeignKey(Proposal, models.CASCADE, 'work_order')
    personal = models.ManyToManyField(
        'accounts.User', related_name='work_order'
    )
    vehicles = models.ManyToManyField(Vehicle, related_name='work_order')
    devices = models.ManyToManyField(LabDevice, related_name='work_order')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    goal = models.TextField(null=True, blank=True)
    file = models.FileField(null=True)
