# Generated by Django 4.2.2 on 2023-07-10 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0023_alter_eventranking_h2h_win_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_IND',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event_H2H',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('is_high_score_wins', models.BooleanField(default=True)),
                ('max_score', models.IntegerField(default=21)),
                ('min_score', models.IntegerField(default=0)),
                ('n_matches', models.PositiveIntegerField()),
                ('n_active_limit', models.PositiveIntegerField(blank=True, null=True)),
                ('n_bracket_teams', models.PositiveIntegerField(default=4)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=False)),
                ('is_round_robin_complete', models.BooleanField(default=False)),
                ('is_concluded', models.BooleanField(default=False)),
                ('brolympics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='brolympics.brolympics')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='bracket_4',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='brolympics.event_h2h'),
        ),
        migrations.AlterField(
            model_name='bracketmatchup',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_h2h_comps', to='brolympics.event_h2h'),
        ),
        migrations.AlterField(
            model_name='competition_h2h',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_h2h_comps', to='brolympics.event_h2h'),
        ),
        migrations.AlterField(
            model_name='competition_ind',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ind_comp', to='brolympics.event_h2h'),
        ),
        migrations.AlterField(
            model_name='eventranking_h2h',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_h2h_event_rankings', to='brolympics.event_h2h'),
        ),
        migrations.AlterField(
            model_name='eventranking_ind',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_ind_event_rankings', to='brolympics.event_ind'),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
