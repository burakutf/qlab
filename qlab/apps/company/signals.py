from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone

from qlab.apps.company.models import (
    CompanyNote,
    LabDevice,
    ProposalChoices,
    WorkOrder,
)


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


def update_company_notes(date, note_prefix, company_name, goal):
    company_note, created = CompanyNote.objects.get_or_create(date=date)
    company_note.notes = (
        note_prefix
        + f': {company_name} Firması {goal} Amaçlı keşif.'
        + (company_note.notes or '')
    )
    company_note.save()


@receiver(post_save, sender=WorkOrder)
def user_notification(instance, created, *args, **kwargs):
    if not created:
        return
    instance.proposal.status = ProposalChoices.WORKORDER
    instance.proposal.save()

    company_name = instance.proposal.company.name
    goal = instance.goal

    update_company_notes(
        instance.start_date, 'Keşif Başlangıç', company_name, goal
    )
    update_company_notes(instance.end_date, 'Keşif Bitiş', company_name, goal)
