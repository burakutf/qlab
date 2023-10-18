# Generated by Django 4.2.5 on 2023-10-18 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
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
                ('title', models.CharField(max_length=64, null=True)),
                ('text', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'medium',
                    models.CharField(
                        choices=[('sms', 'Sms'), ('email', 'Email')],
                        default='email',
                        max_length=5,
                        verbose_name='Kanal',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
