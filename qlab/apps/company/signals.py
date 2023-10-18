from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone

from qlab.apps.company.models import LabDevice

@receiver(pre_save, sender=LabDevice)
def lab_device_pre_save(sender, instance, **kwargs):
    start_date = instance.start_date + timezone.timedelta(days=1)
    existing_devices = LabDevice.objects.filter(
        name=instance.name,
        start_date__lte=start_date,
        finish_date__gte=start_date,
    ).exclude(id=instance.id)

    if existing_devices.exists():
        raise ValidationError(
            'Aynı tarih aralığına sahip bir LabDevice zaten var.'
        )

    if not instance.finish_date:
        instance.finish_date = instance.start_date + timezone.timedelta(
            days=instance.period
        )

@receiver(post_save, sender=LabDevice)
def lab_device_post_save(sender, instance, created, **kwargs):
    if not created and instance.finish_date and instance.finish_date <= timezone.now().date():
        sender.objects.create(
            user=instance.user,
            name=instance.name,
            serial_number=instance.serial_number,
            start_date=instance.finish_date,
            period=instance.period,
        )
