# Generated by Django 4.2.2 on 2023-07-22 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_email_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_phone_verified',
        ),
    ]
