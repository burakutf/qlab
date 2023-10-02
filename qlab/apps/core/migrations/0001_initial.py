# Generated by Django 4.2.5 on 2023-10-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('email', models.EmailField(max_length=254)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
