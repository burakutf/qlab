from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from qlab.apps.core.models import Notification

from .models import User


@receiver(post_save, sender=User)
def user_notification(instance, created, *args, **kwargs):
    if not created:
        return

    Notification.objects.create(
        user=instance,
        title='Qlab Giriş Bilgileri',
        text=f"""
            <h1>Qlab'a Hoş Geldiniz!</h1>
            <p>Merhaba {instance.full_name},</p>
            <p>Qlab'a hoş geldiniz. Aşağıdaki bilgilerle giriş yapabilirsiniz:</p>
            <ul>
                <li>Kullanıcı Adı: {instance.username}</li>
                <li>Parola: {instance.password}</li>
            </ul>
            <p>Giriş yapmak için lütfen <a href="{settings.ALLOWED_HOSTS[0]}">buraya</a> tıklayın.</p>
            <p>Keyifli kullanımlar dileriz!</p>
        """,
    )
