# Generated by Django 4.2.2 on 2023-07-13 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0033_rename_ranking_eventranking_ind_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition_ind',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition_ind',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
