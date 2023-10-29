from django.db import models


from phonenumber_field.modelfields import PhoneNumberField

from qlab.apps.core.utils.set_path import SetPathAndRename


class ProposalChoices(models.IntegerChoices):
    SENDING = 0, ('Teklif Gönderildi')
    APPROVAL = 1, ('Teklif Onaylandı')
    REJECT = 2, ('Teklif Kabul Edilmedi')
    TRANSACTION_CANCELED = 3, ('İşlem İptal Edildi')
    TRANSACTION_ACCEPT = 4, ('İşlem Kabul Edildi')


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tax_number = models.CharField(max_length=10, null=True, blank=True)
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


class LabDevice(models.Model):
    user = models.ForeignKey('accounts.User', models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    serial_number = models.CharField(max_length=128)
    # TODO devicehistory taşıncak date aralığı
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
    user = models.ForeignKey('accounts.User', models.SET_NULL, null=True)
    company = models.ForeignKey(Company, models.SET_NULL, null=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)

class CompanyNote(models.Model):
    notes = models.JSONField()
    date = models.DateField()
