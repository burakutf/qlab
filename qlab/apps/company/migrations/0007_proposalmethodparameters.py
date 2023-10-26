# Generated by Django 4.2.5 on 2023-10-26 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_delete_proposalmethodparameters'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalMethodParameters',
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
                ('count', models.SmallIntegerField()),
                ('method_name', models.JSONField(null=True)),
                (
                    'parameter',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='company.methodparameters',
                    ),
                ),
                (
                    'proposal',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='company.proposal',
                    ),
                ),
            ],
        ),
    ]
