# Generated by Django 4.2.7 on 2023-11-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_workorder_barcode_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodparameters',
            name='current_barcode',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
