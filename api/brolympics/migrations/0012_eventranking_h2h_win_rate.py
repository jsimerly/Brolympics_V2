# Generated by Django 4.2.2 on 2023-07-09 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0011_bracket_4_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventranking_h2h',
            name='win_rate',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
