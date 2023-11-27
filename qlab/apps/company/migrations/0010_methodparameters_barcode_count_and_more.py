# Generated by Django 4.2.7 on 2023-11-27 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_proposalmethodparameters_source_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodparameters',
            name='barcode_count',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='methodparameters',
            name='sample_type',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
