# Generated by Django 4.2.2 on 2023-07-23 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0006_brolympics_img_brolympics_players_league_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brolympics',
            name='hashid',
        ),
        migrations.RemoveField(
            model_name='league',
            name='hashid',
        ),
        migrations.RemoveField(
            model_name='team',
            name='hashid',
        ),
        migrations.AddField(
            model_name='brolympics',
            name='uuid',
            field=models.UUIDField(default=1, editable=False, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='league',
            name='uuid',
            field=models.UUIDField(default=1, editable=False, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='uuid',
            field=models.UUIDField(default=1, editable=False, unique=True),
            preserve_default=False,
        ),
    ]
