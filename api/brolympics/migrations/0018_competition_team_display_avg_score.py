# Generated by Django 4.2.2 on 2023-07-26 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0017_rename_is_concluded_event_h2h_is_complete_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition_team',
            name='display_avg_score',
            field=models.BooleanField(default=True),
        ),
    ]