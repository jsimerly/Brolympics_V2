# Generated by Django 4.2.2 on 2023-06-29 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_user_is_staff_user_prefernce_newsletter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='prefernce_newsletter',
        ),
        migrations.RemoveField(
            model_name='user',
            name='prefernce_recieve_emails',
        ),
    ]