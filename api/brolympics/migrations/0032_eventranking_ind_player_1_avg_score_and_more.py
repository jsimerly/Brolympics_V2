# Generated by Django 4.2.2 on 2023-07-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0031_rename_player_1_score_eventranking_ind_player_1_total_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventranking_ind',
            name='player_1_avg_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventranking_ind',
            name='player_2_avg_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventranking_ind',
            name='team_avg_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
