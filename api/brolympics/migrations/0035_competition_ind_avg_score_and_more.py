# Generated by Django 4.2.2 on 2023-07-14 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0034_competition_ind_end_time_competition_ind_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition_ind',
            name='avg_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition_ind',
            name='display_avg_score',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='event_ind',
            name='display_avg_scores',
            field=models.BooleanField(default=True),
        ),
    ]
