# Generated by Django 4.2.5 on 2023-10-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Company',
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
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('tax_number', models.CharField(max_length=10)),
                ('authorized_person', models.CharField(max_length=50)),
                ('contact_info', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
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
                ('plate', models.CharField(max_length=10)),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('inspection_date', models.DateField(blank=True, null=True)),
                ('insurance_date', models.DateField()),
                ('maintenance_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
