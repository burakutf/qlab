from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.postgres.fields import ArrayField
from django.forms import MultipleChoiceField

from qlab.apps.core.utils.send_email import send_html_mail

# Create your models here.


class AuthAttempt(models.Model):
    """
    Keeping to attempts of login, register, forgot password etc.
    """

    ip = models.GenericIPAddressField()
    username = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)


class Mediums(models.TextChoices):
    SMS = 'sms'
    EMAIL = 'email'
    NOTIFICATION = 'notification'


class Notification(models.Model):
    user = models.ForeignKey('accounts.User', models.CASCADE, null=True)
    title = models.CharField(max_length=128, null=True)
    text = models.TextField(null=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    medium = models.CharField(
        'Kanal',
        max_length=16,
        choices=Mediums.choices,
        default=Mediums.NOTIFICATION,
    )

    def __str__(self):
        return f'{self.user} - {self.title}'

    def save(self, *args, **kwargs):
        if self.medium == Mediums.EMAIL:
            self._send_email()
        elif self.medium == Mediums.SMS:
            # self._send_sms()
            pass
        super().save(*args, **kwargs)

    def _send_email(self):
        if self.user.email:
            send_html_mail(
                subject=f'{self.title}',
                recipient_list=(self.user.email,),
                html_content=f'{self.text}',
            )
        else:
            ValidationError('Kullanıcının geçerli bir e-posta adresi yok.')

    # def _send_sms(self):
    #     raise ValidationError('Sms Pek Yakında Eklenecek!')


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        widget = FilteredSelectMultiple(self.verbose_name, False)
        defaults = {
            'form_class': MultipleChoiceField,
            'widget': widget,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)
