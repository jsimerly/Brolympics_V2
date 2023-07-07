from django.db import models
from django.contrib.auth import get_user_model
import random
from django.utils import timezone

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
    name = models.CharField(max_length=60)

    is_registration_open = models.BooleanField(default=True)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    winner = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='winner'
    )

    def get_available_teams(self):
        return self.teams.filter(available=True)
    
    def _is_duplicate(self, team_1, team_2, pairs_set):
        return (team_1, team_2) in pairs_set or (team_2, team_1) in pairs_set
    
    def _is_comp_map_full(self, comp_map, target_n):
        if not comp_map:
            return False
        
        for value in comp_map.values():
            if value != target_n:
                return False
        return True
    
    def create_team_pairs(self):
        unique_pairs = []
        teams = list(self.teams.all())

        for i in range(1, len(teams)):
            for j in range(i):
                unique_pairs.append(teams[i], teams[j])

        while True:
            tracking_map = {}
            selected_sets = []
            random.shuffle(unique_pairs)

            for team_pair in unique_pairs:
                team_1 = team_pair[0]
                team_2 = team_pair[1]

                if team_1 not in tracking_map:
                    tracking_map[team_1] = 0

                if team_2 not in tracking_map:
                    tracking_map[team_2] = 0

                if tracking_map[team_1] < 4 and tracking_map[team_2] < 4:
                    selected_sets.append(team_pair)
                    tracking_map[team_1] += 1
                    tracking_map[team_2] += 1

            if self._is_comp_map_full(tracking_map, 4):
                return selected_sets
            
    def update_overall_rankings(self):
        pass 
    #this will need to inclue both h2h and ind so likely 2 seperate queries

    def _create_ranking_objs(self):
        rankings = [
            OverallBrolympicsRanking(brolympics=self, team=team)
            for team in self.teams.all()
        ]
        OverallBrolympicsRanking.objects.bulk_create(rankings)

    def start(self):
        self.start_time = timezone.now()
        self.registration_open = False
        self._create_ranking_objs()
        self.save()

    def end(self):
        self.end_time = timezone.now()
        #finish ending

class OverallBrolympicsRanking(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        related_name='overall_ranking'
    )
    rank = models.PositiveIntegerField(default=1)
    team = models.ForeignKey(
        'Team',
        on_delete=models.PROTECT,
    )

    total_score = models.PositiveIntegerField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

EVENT_CHOICES = (
    ('H', 'Head to Head'),
    ('I', 'Individual'),
    ('T', 'Team Score'),
)
class Event(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        related_name='events'
    )

    name = models.CharField(max_length=60)
    type = models.CharField(max_length=1, choices=EVENT_CHOICES, default='H')

    is_high_score_wins = models.BooleanField(default=True)
    max_score = models.IntegerField(default=0)
    min_score = models.IntegerField(blank=True, null=True)

    n_active_limit = models.PositiveIntegerField(blank=True, null=True)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_available = models.BooleanField(default=False)
    is_round_robin_complete = models.BooleanField(default=False)

    is_concluded = models.BooleanField(default=False)

    def create_competition_objs_h2h(self):
        pairs = self.brolympics.create_team_pairs()
        competitions = [
            Competition_H2H(event=self, team_1=pair[0], team_2=pair[1])
            for pair in pairs
        ]
        Competition_H2H.objects.bulk_create(competitions)


    def create_competition_objs_ind(self):
        individuals_scores = True
        if self.type == 'T':
            individuals_scores = False
            
        competitions = [
            Competition_Ind(event=self, team=team, individuals_scores=individuals_scores)
            for team in self.brolympics.teams.all()
        ]

        Competition_Ind.objects.bulk_create(competitions)

    def create_event_ranking_h2h(self):
        ranking_objs = [
            EventRanking_H2H(event=self, team=team)
            for team in self.brolympics.teams.all()
        ]
        EventRanking_H2H.objects.bulk_create(ranking_objs)

    def create_event_ranking_ind(self):
        ranking_objs = [
            EventRanking_Ind(event=self, team=team)
            for team in self.brolympics.team.all()
        ]
        EventRanking_Ind.objects.bulk_create(ranking_objs)

    def create_bracket():
        pass


    def _start_h2h(self):
        self.create_competition_objs_h2h()
        self.create_event_ranking_h2h()
        self.create_bracket()

    def _start_ind(self):
        self.create_competition_objs_ind()
        self.create_event_ranking_ind()


    def start(self):
        self.start_time = timezone.now()
        self.available = True

        if self.type == 'H':
            self._start_h2h()
        if self.type == 'I' or self.type=='T':
            self._start_ind()


class Team(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        null=False,
        related_name='teams'
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

    is_available = models.BooleanField(default=False)

    score = models.PositiveIntegerField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

class Competition_Ind(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='ind_comp',
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='ind_competition_team',
    )

    is_individual_scores = models.BooleanField(default=True)
    player_1_score = models.IntegerField(blank=True, null=True)
    player_2_score = models.IntegerField(blank=True, null=True)

    team_score = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)


class Competition_H2H_Base(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='%(class)s_h2h_comps'
    )

    team_1 = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_h2h_comp_team_1',
        null=True, # allowed to be null because this is also used in bracket
        blank=True
    )

    team_2 = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_h2h_comp_team_2',
        null=True,
        blank=True
    )

    team_1_score = models.IntegerField(blank=True, null=True)
    team_2_score = models.IntegerField(blank=True, null=True)

    winner = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_h2h_comp_wins',
        null=True,
        blank=True,
        default=None
    )
    loser = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_h2h_comp_losses',
        null=True,
        blank=True,
        default=None
    )

    active = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Competition_H2H(Competition_H2H_Base):
   pass



class EventRanking_Ind(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_ind_event_rankings'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='team_ind_event_rankings'
    )

    is_individual_scores = models.BooleanField(default=True)
    player_1_score = models.IntegerField(blank=True, null=True)
    player_2_score = models.IntegerField(blank=True, null=True)
    
    team_score = models.IntegerField(blank=True, null=True)
    
    ranking = models.PositiveIntegerField(default=1)
    earned_points = models.PositiveIntegerField(default=0)

    is_final = models.BooleanField(default=False)

class EventRanking_H2H(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_h2h_event_rankings'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='team_h2h_event_rankings'
    )

    rank = models.PositiveIntegerField(default=1)
    earned_points = models.PositiveIntegerField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

    score_for = models.IntegerField(default=0)
    score_against = models.IntegerField(default=0)

    sos_wins = models.PositiveIntegerField(default=0)
    sos_losses = models.PositiveIntegerField(default=0)
    sos_ties = models.PositiveIntegerField(default=0)

    is_final = models.BooleanField(default=False)


class BracketMatchup(Competition_H2H_Base):
    bracket = models.ForeignKey(
        'Bracket_4',
        on_delete=models.CASCADE
    )

    winner_node = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='won_matchups'
    )

    loser_node = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lost_matchups'
    )

    left = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='right_matchups'
    )
    right = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='left_matchups'
    )
    
    team_1_seed = models.PositiveIntegerField(null=True, blank=True)
    team_2_seed = models.PositiveIntegerField(null=True, blank=True)
    
    def update_teams(self, higher_seed, lower_seed):
        self.team_1 = higher_seed
        self.team_2 = lower_seed

    def start(self, player):
        if self.bracket.is_active:
            super().start(player)

    def end(self, team_1_score, team_2_score):
        if not self.winner or not self.loser:
            raise 

        super().end(team_1_score, team_2_score)

        if self.winner_node.team_1 is None:
            self.winner_node.team_1 = self.winner
            self.winner_node.team_1_seed = self.team_1_seed
        else:
            self.winner_node.team_2 = self.winner
            self.winner_node.team_2_seed = self.team_2_seed
        
        if self.loser_node.team_1 is None:
            self.loser_node.team_1 = self.loser
            self.loser_node.team_1_seed = self.team_1_seed
        else:
            self.loser_node.team_2 = self.loser
            self.loser_node.team_2 = self.team_2_seed

        if self == self.bracket.championship:
            self.bracket.is_active = False
            self.bracket.is_completed = True
            return

class Bracket_4(models.Model):
    n_player = models.PositiveIntegerField(default=4)
    
    championship = models.ForeignKey(
        BracketMatchup,
        on_delete=models.CASCADE,
        related_name='root'
    )

    loser_bracket_finals = models.ForeignKey(
        BracketMatchup,
        on_delete=models.CASCADE,
        related_name='loser_root'
    )
    
    is_active = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_losers_bracket = models.BooleanField(default=True)

    def create(self):
        championship = BracketMatchup.objects.create(bracket=self)
        third = BracketMatchup.objects.create(bracket=self)

        one_four = BracketMatchup.objects.create(
            bracket=self, 
            team_1_seed=1, 
            team_2_seed=4, 
            winner_node=championship,
            loser_node=third
        )
        two_three = BracketMatchup.objects.create(
            bracket=self, 
            team_1_seed=2, 
            team_2_seed=3,
            winner_node=championship,
            loser_node=third
        )

        championship.left = one_four
        championship.right = two_three

        self.championship = championship #root
        self.save()
        

    






