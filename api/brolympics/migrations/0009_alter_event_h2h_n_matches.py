# Generated by Django 4.2.2 on 2023-07-23 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0008_alter_brolympics_uuid_alter_league_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_h2h',
            name='n_matches',
            field=models.PositiveIntegerField(default=4),
        ),
    ]
