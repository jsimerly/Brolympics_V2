# Generated by Django 4.2.2 on 2023-07-10 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0021_alter_eventranking_h2h_win_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventranking_h2h',
            name='win_rate',
            field=models.FloatField(),
        ),
    ]
