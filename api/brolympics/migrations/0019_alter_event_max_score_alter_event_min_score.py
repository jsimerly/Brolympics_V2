# Generated by Django 4.2.2 on 2023-07-09 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0018_alter_bracketmatchup_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='max_score',
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name='event',
            name='min_score',
            field=models.IntegerField(default=0),
        ),
    ]
