from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class League(models.Model):
    name = models.CharField(max_length=120)
    league_owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False
    )
    founded = models.DateTimeField(auto_now_add=True)

class Brolympics(models.Model):
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        null=False
    )

    n_teams = models.PositiveIntegerField(default=0)

    started = models.DateTimeField(blank=True)
    ended = models.DateTimeField(blank=True)
    completed = models.BooleanField(default=False)

    winner = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='winner'
    )

EVENT_CHOICES = (
    ('H', 'Head to Head'),
    ('I', 'Individual'),
)

class Event(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        related_name='event'
    )

    name = models.CharField(max_length=60)
    type = models.CharField(max_length=1, choices=EVENT_CHOICES, default='H')

    high_score_wins = models.BooleanField(default=True)
    max_score = models.IntegerField()
    min_score = models.IntegerField()

    n_active_limit = models.PositiveIntegerField()
    concluded = models.BooleanField()

class OverallBrolympicsRanking(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        related_name='overall_ranking'
    )
    ranking = models.PositiveIntegerField(default=1)
    team = models.ForeignKey(
        'Team',
        on_delete=models.PROTECT,
    )

    total_score = models.PositiveIntegerField()
    win_rate = models.PositiveIntegerField()
    
class Team(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        null=False,
        related_name='team'
    )

    name = models.CharField(max_length=120)
    team_picture = models.ImageField()

    player_1 = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name='player_1_set'
    )

    player_2 = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name='player_2_set'
    )

    score = models.PositiveIntegerField()

    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    ties = models.PositiveIntegerField()

class IndividualCompetition(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='ind_comp'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='ind_competition_team'
    )

    player_1_score = models.IntegerField()
    player_2_score = models.IntegerField()

    active = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)


class H2hCompetition(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='h2h_comp'
    )

    team_1 = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='h2h_comp_team_1'
    )

    team_2 = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='h2h_comp_team_2'
    )

    team_1_score = models.IntegerField()
    team_2_score = models.IntegerField()

    active = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

class EventRanking_Individual(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_ranking_ind'
    )

    ranking = models.PositiveIntegerField()
    earned_points = models.PositiveIntegerField()

    team_score = models.PositiveIntegerField()
    final = models.BooleanField(default=False)

class EventRanking_H2H(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_ranking_h2h'
    )

    ranking = models.PositiveIntegerField()
    earned_points = models.PositiveIntegerField()

    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    ties = models.PositiveIntegerField()

    final = models.BooleanField(default=False)
