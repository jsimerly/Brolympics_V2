# Generated by Django 4.2.2 on 2023-07-07 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brolympics', '0009_remove_bracketmatchup_competition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bracket_4',
            name='championship',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='root', to='brolympics.bracketmatchup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bracket_4',
            name='loser_bracket_finals',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='loser_root', to='brolympics.bracketmatchup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_h2h_comps', to='brolympics.event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='left',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='right_matchups', to='brolympics.bracketmatchup'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='loser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_losses', to='brolympics.team'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='loser_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lost_matchups', to='brolympics.bracketmatchup'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='right',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left_matchups', to='brolympics.bracketmatchup'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_team_1', to='brolympics.team'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='team_1_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_team_2', to='brolympics.team'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='team_2_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_wins', to='brolympics.team'),
        ),
        migrations.AddField(
            model_name='bracketmatchup',
            name='winner_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_matchups', to='brolympics.bracketmatchup'),
        ),
        migrations.AlterField(
            model_name='bracketmatchup',
            name='team_1_seed',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bracketmatchup',
            name='team_2_seed',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competition_h2h',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_h2h_comps', to='brolympics.event'),
        ),
        migrations.AlterField(
            model_name='competition_h2h',
            name='loser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_losses', to='brolympics.team'),
        ),
        migrations.AlterField(
            model_name='competition_h2h',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_team_1', to='brolympics.team'),
        ),
        migrations.AlterField(
            model_name='competition_h2h',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_team_2', to='brolympics.team'),
        ),
        migrations.AlterField(
            model_name='competition_h2h',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_h2h_comp_wins', to='brolympics.team'),
        ),
    ]
