# Generated by Django 4.2.2 on 2023-06-29 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_admin_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='user',
            name='prefernce_newsletter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='prefernce_recieve_emails',
            field=models.BooleanField(default=False),
        ),
    ]