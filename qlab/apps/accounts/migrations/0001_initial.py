# Generated by Django 4.2.5 on 2023-11-15 11:16

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import qlab.apps.core.models
import qlab.apps.core.utils.set_path


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'password',
                    models.CharField(max_length=128, verbose_name='password'),
                ),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    ),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'username',
                    models.CharField(
                        error_messages={
                            'unique': 'A user with that username already exists.'
                        },
                        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name='username',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        blank=True, max_length=150, verbose_name='first name'
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        blank=True, max_length=150, verbose_name='last name'
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name='email address',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='date joined',
                    ),
                ),
                (
                    'full_name',
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    'phone',
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        db_index=True,
                        max_length=128,
                        null=True,
                        region=None,
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False, verbose_name='is staff'
                    ),
                ),
                ('birth_date', models.DateField(blank=True, null=True)),
                (
                    'gender',
                    models.CharField(
                        blank=True,
                        choices=[('MN', 'Erkek'), ('WMN', 'Kadın')],
                        max_length=3,
                        null=True,
                    ),
                ),
                (
                    'permissions',
                    qlab.apps.core.models.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ('user.create', 'KULLANICI OLUŞTUR'),
                                ('user.view', 'KULLANICI GÖRÜNTÜLE'),
                                ('user.update', 'KULLANICI GÜNCELLE'),
                                ('user.destroy', 'KULLANICI SİL'),
                                (
                                    'user_detail.create',
                                    'KULLANICI DETAY OLUŞTUR',
                                ),
                                (
                                    'user_detail.update',
                                    'KULLANICI DETAY GÜNCELLE',
                                ),
                                (
                                    'user_detail.view',
                                    'KULLANICI DETAY GÖRÜNTÜLE',
                                ),
                                ('user_detail.destroy', 'KULLANICI DETAY SİL'),
                                ('group.create', 'GRUP OLUŞTUR'),
                                ('group.view', 'GRUP GÖRÜNTÜLE'),
                                ('group.update', 'GRUP GÜNCELLE'),
                                ('group.destroy', 'GRUP SİL'),
                                ('vehicle.create', 'ARAÇ OLUŞTUR'),
                                ('vehicle.view', 'ARAÇ GÖRÜNTÜLE'),
                                ('vehicle.update', 'ARAÇ GÜNCELLE'),
                                ('vehicle.destroy', 'ARAÇ SİL'),
                                ('company.create', 'FİRMA OLUŞTUR'),
                                ('company.view', 'FİRMA GÖRÜNTÜLE'),
                                ('company.update', 'FİRMA GÜNCELLE'),
                                ('company.destroy', 'FİRMA SİL'),
                                ('method.create', 'METOT OLUŞTUR'),
                                ('method.view', 'METOT GÖRÜNTÜLE'),
                                ('method.update', 'METOT GÜNCELLE'),
                                ('method.destroy', 'METOT SİL'),
                                ('parameter.create', 'PARAMETRE OLUŞTUR'),
                                ('parameter.view', 'PARAMETRE GÖRÜNTÜLE'),
                                ('parameter.update', 'PARAMETRE GÜNCELLE'),
                                ('parameter.destroy', 'PARAMETRE SİL'),
                                ('device.create', 'CİHAZ OLUŞTUR'),
                                ('device.view', 'CİHAZ GÖRÜNTÜLE'),
                                ('device.update', 'CİHAZ GÜNCELLE'),
                                ('device.destroy', 'CİHAZ SİL'),
                                ('draft.create', 'TASLAK OLUŞTUR'),
                                ('draft.view', 'TASLAK GÖRÜNTÜLE'),
                                ('draft.update', 'TASLAK GÜNCELLE'),
                                ('draft.destroy', 'TASLAK SİL'),
                                ('proposal.create', 'TEKLİF OLUŞTUR'),
                                ('proposal.update', 'TEKLİF GÜNCELLE'),
                                ('proposal.view', 'TEKLİF GÖRÜNTÜLE'),
                                ('statistics.view', 'İSTATİSTİK GÖRÜNTÜLE'),
                                ('note.create', 'NOT OLUŞTUR'),
                                ('note.view', 'NOT GÖRÜNTÜLE'),
                                ('note.update', 'NOT GÜNCELLE'),
                                ('note.destroy', 'NOT SİL'),
                            ],
                            max_length=32,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'detail',
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    'criminal_record',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/criminal_record/'
                        ),
                    ),
                ),
                (
                    'military_certificate',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/military_document/'
                        ),
                    ),
                ),
                (
                    'blood_group_certificate',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/blood_group/'
                        ),
                    ),
                ),
                (
                    'driver_certificate',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/driver_certificate/'
                        ),
                    ),
                ),
                (
                    'emission_certificate',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/emission_certificate/'
                        ),
                    ),
                ),
                (
                    'height_certificate',
                    models.FileField(
                        blank=True,
                        help_text='Yüksekte çalışma belgesi',
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/height_certificate/'
                        ),
                    ),
                ),
                (
                    'graduate_certificate',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=qlab.apps.core.utils.set_path.SetPathAndRename(
                            'profile/graduate_certificate/'
                        ),
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=32)),
                (
                    'permissions',
                    qlab.apps.core.models.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ('user.create', 'KULLANICI OLUŞTUR'),
                                ('user.view', 'KULLANICI GÖRÜNTÜLE'),
                                ('user.update', 'KULLANICI GÜNCELLE'),
                                ('user.destroy', 'KULLANICI SİL'),
                                (
                                    'user_detail.create',
                                    'KULLANICI DETAY OLUŞTUR',
                                ),
                                (
                                    'user_detail.update',
                                    'KULLANICI DETAY GÜNCELLE',
                                ),
                                (
                                    'user_detail.view',
                                    'KULLANICI DETAY GÖRÜNTÜLE',
                                ),
                                ('user_detail.destroy', 'KULLANICI DETAY SİL'),
                                ('group.create', 'GRUP OLUŞTUR'),
                                ('group.view', 'GRUP GÖRÜNTÜLE'),
                                ('group.update', 'GRUP GÜNCELLE'),
                                ('group.destroy', 'GRUP SİL'),
                                ('vehicle.create', 'ARAÇ OLUŞTUR'),
                                ('vehicle.view', 'ARAÇ GÖRÜNTÜLE'),
                                ('vehicle.update', 'ARAÇ GÜNCELLE'),
                                ('vehicle.destroy', 'ARAÇ SİL'),
                                ('company.create', 'FİRMA OLUŞTUR'),
                                ('company.view', 'FİRMA GÖRÜNTÜLE'),
                                ('company.update', 'FİRMA GÜNCELLE'),
                                ('company.destroy', 'FİRMA SİL'),
                                ('method.create', 'METOT OLUŞTUR'),
                                ('method.view', 'METOT GÖRÜNTÜLE'),
                                ('method.update', 'METOT GÜNCELLE'),
                                ('method.destroy', 'METOT SİL'),
                                ('parameter.create', 'PARAMETRE OLUŞTUR'),
                                ('parameter.view', 'PARAMETRE GÖRÜNTÜLE'),
                                ('parameter.update', 'PARAMETRE GÜNCELLE'),
                                ('parameter.destroy', 'PARAMETRE SİL'),
                                ('device.create', 'CİHAZ OLUŞTUR'),
                                ('device.view', 'CİHAZ GÖRÜNTÜLE'),
                                ('device.update', 'CİHAZ GÜNCELLE'),
                                ('device.destroy', 'CİHAZ SİL'),
                                ('draft.create', 'TASLAK OLUŞTUR'),
                                ('draft.view', 'TASLAK GÖRÜNTÜLE'),
                                ('draft.update', 'TASLAK GÜNCELLE'),
                                ('draft.destroy', 'TASLAK SİL'),
                                ('proposal.create', 'TEKLİF OLUŞTUR'),
                                ('proposal.update', 'TEKLİF GÜNCELLE'),
                                ('proposal.view', 'TEKLİF GÖRÜNTÜLE'),
                                ('statistics.view', 'İSTATİSTİK GÖRÜNTÜLE'),
                                ('note.create', 'NOT OLUŞTUR'),
                                ('note.view', 'NOT GÖRÜNTÜLE'),
                                ('note.update', 'NOT GÜNCELLE'),
                                ('note.destroy', 'NOT SİL'),
                            ],
                            max_length=32,
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
    ]
