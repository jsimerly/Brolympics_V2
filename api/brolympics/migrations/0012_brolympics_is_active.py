# Generated by Django 4.2.2 on 2023-07-24 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0011_bracket_4_uuid_bracketmatchup_uuid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brolympics',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]