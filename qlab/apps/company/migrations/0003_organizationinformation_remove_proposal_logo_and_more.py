# Generated by Django 4.2.7 on 2023-11-22 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import qlab.apps.core.utils.set_path


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_proposallogo_alter_proposal_company_proposal_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(verbose_name=128)),
                ('name', models.CharField(verbose_name=256)),
                ('address', models.CharField(verbose_name=256)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('mail', models.EmailField(max_length=254)),
                ('signature', models.FileField(blank=True, null=True, upload_to=qlab.apps.core.utils.set_path.SetPathAndRename('signature/'))),
                ('title', models.CharField(max_length=128)),
                ('left_logo', models.ImageField(blank=True, null=True, upload_to=qlab.apps.core.utils.set_path.SetPathAndRename('organization/logo/'))),
                ('right_logo', models.ImageField(blank=True, null=True, upload_to=qlab.apps.core.utils.set_path.SetPathAndRename('organization/logo/'))),
            ],
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='logo',
        ),
        migrations.AlterField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ProposalLogo',
        ),
        migrations.AddField(
            model_name='proposal',
            name='organization_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.organizationinformation'),
        ),
    ]
