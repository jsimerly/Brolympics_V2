from django.db import models
from django.contrib.auth import get_user_model
import random
from django.utils import timezone
from django.db.models import Q

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
    is_complete = models.BooleanField(default=False)

    winner = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='winner'
    )

    def get_available_teams(self):
        return self.teams.filter(is_available=True)
    
    def _is_duplicate(self, team_1, team_2, pairs_set):
        return (team_1, team_2) in pairs_set or (team_2, team_1) in pairs_set
    
            
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
        self.is_registration_open = False
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
    max_score = models.IntegerField(default=21)
    min_score = models.IntegerField(default=0)

    #add validation that it's an even number and no more than n_teams-1
    n_matches = models.PositiveIntegerField(null=False, blank=False)
    n_active_limit = models.PositiveIntegerField(blank=True, null=True)
    n_bracket_teams = models.PositiveIntegerField(default=4)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    is_available = models.BooleanField(default=False)
    is_round_robin_complete = models.BooleanField(default=False)
    is_concluded = models.BooleanField(default=False)

    def start(self):
        self.start_time = timezone.now()
        self.is_available = True

        if self.type == 'H':
            self._start_h2h()
        if self.type == 'I' or self.type=='T':
            self._start_ind()

    def finalize(self):
        self.end_time = timezone.now()
        self.is_available = False
        self.is_concluded = True
        team_rankings = list(self.event_h2h_event_rankings.all())

        bracket_teams = [
            self.bracket_4.championship.winner,
            self.bracket_4.championship.loser,
            self.bracket_4.third_place.winner,
            self.bracket_4.third_place.loser,
        ]
        back_half_teams = team_rankings[len(bracket_teams):]

        final_ranking = bracket_teams  + back_half_teams
        self.update_event_rankings_h2h(final_ranking)

        self.end_time = timezone.now()
        self.is_available = False
        self.is_concluded = True       
            

    def is_bracket_comp_ready(self, bracket_match):
        return bracket_match.is_complete != True and bracket_match.team_1 != None and bracket_match.team_2 != None
    
    def _find_available_bracket_comps(self):
        return BracketMatchup.objects.filter(
            bracket=self.bracket_4,
            team_1__isnull=False,
            team_2__isnull=False,
            is_complete=False
        )
    
    def _find_available_standard_comps(self):
        return Competition_H2H.objects.filter(
            event=self,
            team_1__is_available=True,
            team_2__is_available=True,
        )     

    def find_available_comps(self):
        if self.is_round_robin_complete:
            return self._find_available_standard_comps
        return self._find_available_bracket_comps
    
    def _is_comp_map_full(self, comp_map, target_n):
        if not comp_map:
            return False
        
        for value in comp_map.values():
            if value != target_n:
                return False
        return True 
    
    def create_team_pairs(self):
        unique_pairs = []
        teams = list(self.brolympics.teams.all())

        for i in range(1, len(teams)):
            for j in range(i):
                unique_pairs.append([teams[i], teams[j]])

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

                if tracking_map[team_1] < self.n_matches and tracking_map[team_2] < self.n_matches:
                    selected_sets.append(team_pair)
                    tracking_map[team_1] += 1
                    tracking_map[team_2] += 1

            if self._is_comp_map_full(tracking_map, self.n_matches):
                return selected_sets


    def create_competition_objs_h2h(self):
        pairs = self.create_team_pairs()
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

    def create_bracket(self):
        bracket_obj = Bracket_4.objects.create(event=self)
        bracket_obj.create_matchups()


    def _start_h2h(self):
        self.create_competition_objs_h2h()
        self.create_event_ranking_h2h()
        self.create_bracket()

    def _start_ind(self):
        self.create_competition_objs_ind()
        self.create_event_ranking_ind()


    def get_score_to_rank(self):
        n_teams = len(self.brolympics.teams.all())
        score_map = {
            1 : n_teams+2,
            2 : n_teams,
            3 : n_teams-1,
        }

        for i in range(3, n_teams):
            score_map[i+1] = n_teams-i

        return score_map
           

    def set_rankings_and_points(self, team_rankings):
        score_map = self.get_score_to_rank()

        tied_teams = []
        tied_teams_points = 0
        prior_win_rate = -1
        tied_ranking = self.n_bracket_teams + 1

        for i, ranking in enumerate(team_rankings):
            if i < self.n_bracket_teams:
                ranking.rank = i + 1
                ranking.points = score_map[i+1]
            else:
                if prior_win_rate == -1 or ranking.win_rate == prior_win_rate:
                    tied_teams.append(ranking)
                    tied_teams_points += score_map[i+1]
                else:
                    split_points = tied_teams_points/len(tied_teams_points)
                    for team in tied_teams:
                        team.rank = tied_ranking
                        team.points = split_points

                        tied_teams = [ranking]

                        tied_teams_points = score_map[i+1]
                        tied_ranking = i+1

                prior_win_rate = ranking.win_rate

        if tied_teams:
            split_points = tied_teams_points/len(tied_teams)
            for team in tied_teams:
                team.rank = tied_ranking
                team.points = split_points

    def update_event_rankings_h2h(self, team_rankings=None):
        if team_rankings == None:
            team_rankings = list(self.event_h2h_event_rankings.all())
        team_rankings = sorted(team_rankings, key=lambda x: x.win_rate, reverse=True)

        tie_broken_teams = self.break_tie(team_rankings)
        self.set_rankings_and_points(tie_broken_teams)

        update_fields = [
            'rank', 'points'
        ]

        EventRanking_H2H.objects.bulk_update(
            team_rankings, update_fields
        )



    def full_update_event_rankings_h2h(self):
        completed_comps = self._get_completed_event_comps_h2h()
        team_rankings = list(self.event_h2h_event_rankings.all())

        for ranking in team_rankings:
            self._wipe_win_loss_sos_h2h(ranking)
        
        for comp in completed_comps:
            self._update_ranking_score_and_sos_h2h(comp, team_rankings)

        self.update_event_rankings_h2h(team_rankings)


    def flatten_1(self, lst):
        result = []
        for i in lst:
            if isinstance(i, list):
                result.extend(self.flatten_1(i))
            else:
                result.append(i)
        return result


    def flatten_2(self, lst):
        holder = []
        self._flatten_2(lst, holder)

        return holder


    def _flatten_2(self, element, result, parent_element=None):
        if not isinstance(element, list):
            if parent_element not in result:
                result.append(parent_element)
        else:
            for nested_element in element:
                self._flatten_2(nested_element, result, element)

    def _is_tie_broken(self, tied_teams):
        for group in tied_teams:
            if len(group) != 1:
                return False
        return True

    def _get_ordered_teams(self, sorted_teams):
        break_value_count_teams = {}
        ordered_teams = []

        for team, value in sorted_teams:
            if value not in break_value_count_teams:
                break_value_count_teams[value] = []
            break_value_count_teams[value].append(team)

        for value in sorted(break_value_count_teams.copy().keys(), reverse=True):
            ordered_teams.append(break_value_count_teams[value])

        return ordered_teams

    def _tie_break_manager(self, tied_teams, tie_break_order_funcs):
        if len(tied_teams) <= 1:
            return tied_teams
        
        ordered_nested_teams=tied_teams
        for tie_breaker in tie_break_order_funcs:
            groups = []
            for group in ordered_nested_teams:
                group = tie_breaker(group)

                ordered_group = self._get_ordered_teams(group)
                groups.append(ordered_group)

            if self._is_tie_broken(ordered_nested_teams):
                break

        return ordered_nested_teams


    def break_tie(self, team_rankings):
        grouped_teams = self._group_by_win_rate(team_rankings)

        tie_break_order = [
            self._break_head_to_head__wins,
            self._break_won_games_total,
            self._break_victory_margin,
            self._break_strength_of_schedule,
            self._break_strength_of_schedule_wins
        ]

        ordered_nested_teams = self._tie_break_manager(grouped_teams, tie_break_order)

        if not self._is_tie_broken(ordered_nested_teams):
            for tied_group in ordered_nested_teams:
                random.shuffle(tied_group)

        
        return self.flatten_1(ordered_nested_teams) #full flatten the list

    def _group_by_win_rate(self, teams):
        win_rate_to_teams = {}

        for team in teams:
            win_rate = team.win_rate
            if win_rate not in win_rate_to_teams:
                win_rate_to_teams[win_rate] = []
            win_rate_to_teams[win_rate].append(team)

        return list(win_rate_to_teams.values())
    
    def _break_head_to_head__wins(self, teams):
        tied_team_ids = [team.id for team in teams]
        
        head_to_head_comps = Competition_H2H.objects.filter(
            event=self,
            is_complete=True,
            team_1__in=tied_team_ids,
            team_2__in=tied_team_ids
        )

        team_h2h_wins_map = {team: 0 for team in teams}
        for comp in head_to_head_comps:
            team_h2h_wins_map[comp.winner] += 1

        sorted_by_head_to_head_wins = sorted(team_h2h_wins_map.items(), key=lambda x: x[1], reverse=True)

        return sorted_by_head_to_head_wins

    def _break_won_games_total(self, teams):
        event_wins = {}

        for team in teams:
            event_wins[team] = team.wins

        sorted_by_event_wins = sorted(event_wins.items(), key=lambda x: x[1], reverse=True)
        return sorted_by_event_wins

    def _break_victory_margin(self, teams):
        margin_of_victory = {}
        
        for team in teams:
            margin_of_victory[team] = team.score_for - team.score_against
        
        sorted_by_margin_of_victory = sorted(margin_of_victory.items(), key=lambda x: x[1], reverse=True)
        return sorted_by_margin_of_victory

    def _break_strength_of_schedule(self, teams):
        strength_of_schedule = {}
        for team in teams:
            if (team.sos_wins + team.sos_losses + team.sos_ties) > 0:
                strength_of_schedule[team] = (team.sos_wins + (team.sos_ties * 0.5)) + (team.sos_wins + team.sos_losses + team.sos_ties)
            else:
                strength_of_schedule[team] = 1
        
        sorted_by_strength_of_schedule = sorted(strength_of_schedule.items(), key=lambda x: x[1], reverse=True)
        return sorted_by_strength_of_schedule

    def _break_strength_of_schedule_wins(self, teams):
        stength_of_schedule_vic = {}

        for team in teams:
            stength_of_schedule_vic[team] = team.sos_wins
        
        sorted_by_strength_of_schedule_vic = sorted(stength_of_schedule_vic.items(), key=lambda x: x[1], reverse=True)
        return sorted_by_strength_of_schedule_vic

    def get_top_teams_h2h(self, team_rankings):
        top_teams = []
        top_cutoff_win_rate = team_rankings[self.n_bracket_teams-1].win_rate

        for i in range(len(team_rankings)):
            if i < self.n_bracket_teams:
                top_teams.append(team_rankings[i])

            if team_rankings[i].win_rate == top_cutoff_win_rate:
                top_teams.append(team_rankings[i])
            else:
                break
        return top_teams


    def _update_ranking_score_and_sos_h2h(self, comp, team_rankings):
        team_1_ranking = next((r for r in team_rankings if r.team == comp.team_1), None)
        team_2_ranking = next((r for r in team_rankings if r.team == comp.team_2), None)

        if comp.winner == None and comp.loser == None:
            team_1_ranking.ties += 1
            team_2_ranking.ties += 1
        else:
            winner_ranking = next((r for r in team_rankings if r.team == comp.winner), None)
            loser_ranking = next((r for r in team_rankings if r.team == comp.loser), None)

            if winner_ranking:
                winner_ranking.wins += 1
            else:
                loser_ranking.losses += 1

        team_1_ranking.score_for += comp.team_1_score
        team_1_ranking.score_against += comp.team_2_score
        team_2_ranking.score_for += comp.team_2_score
        team_2_ranking.score_against += comp.team_1_score
                    

    def _wipe_win_loss_sos_h2h(self, ranking):
        ranking.wins = 0
        ranking.losses = 0
        ranking.ties = 0

        ranking.score_for = 0
        ranking.score_against = 0

        ranking.sos_wins = 0
        ranking.sos_losses = 0
        ranking.sos_ties = 0
    
    def _get_completed_event_comps_h2h(self):
        return Competition_H2H.objects.filter(
            event=self,
            is_complete=True,
        )
    
    def check_for_round_robin_completion(self):
        if self.start_time == None or self.is_round_robin_complete:
            return
        
        uncompleted = Competition_H2H.objects.filter(event=self, is_complete=False)
        if len(uncompleted) == 0:
            self.is_round_robin_complete = True
            self.update_bracket()
            self.save()

    def update_bracket(self):
        top_4_rankings = self.event_h2h_event_rankings.all().order_by('rank')[:self.n_bracket_teams]
        self.bracket_4.update_teams(top_4_rankings)


class Team(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        null=True,
        related_name='teams'
    )

    name = models.CharField(max_length=120)
    team_picture = models.ImageField(null=True, blank=True)

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

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def determine_winner(self):
        if self.team_1_score == self.team_2_score:
            winner, loser = None, None
        elif (self.team_1_score > self.team_2_score) == self.event.is_high_score_wins:
            winner, loser = self.team_1, self.team_2
        else:
            winner, loser = self.team_2, self.team_1
        
        return winner, loser
    

    def start(self):
        self.start_time = timezone.now()
        self.is_active = True
        self.team_1.is_available, self.team_2.is_available = False, False

        self.save()

    def end(self, team_1_score, team_2_score):
        self.end_time = timezone.now()
        self.team_1.is_available, self.team_2.is_available = True, True

        self.team_1_score = team_1_score
        self.team_2_score = team_2_score

        winner, loser = self.determine_winner()

        self.winner = winner
        self.loser = loser

        team_1_ranking = EventRanking_H2H.objects.get(event=self.event, team=self.team_1)
        team_2_ranking = EventRanking_H2H.objects.get(event=self.event, team=self.team_2)

        if team_1_ranking.team == winner:
            team_1_ranking.wins += 1
            team_2_ranking.losses += 1
        elif team_2_ranking.team == winner:
            team_1_ranking.losses += 1
            team_2_ranking.wins += 1
        else:
            team_1_ranking.ties += 1
            team_2_ranking.ties += 1

        team_1_ranking.score_for += team_1_score
        team_1_ranking.score_against += team_2_score
        team_2_ranking.score_for += team_2_score
        team_2_ranking.score_against += team_1_score
        
        team_1_ranking.win_rate = team_1_ranking.get_win_rate()
        team_2_ranking.win_rate = team_2_ranking.get_win_rate()

        team_1_ranking.save()
        team_2_ranking.save()

        self.is_complete=True
        self.is_active=False

        self.save()

class Competition_H2H(Competition_H2H_Base):
    def end(self, team_1_score, team_2_score):
        super().end(team_1_score, team_2_score)
        self.event.update_event_rankings_h2h()

       

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
    points = models.PositiveIntegerField(default=0)

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
    points = models.PositiveIntegerField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    win_rate = models.FloatField(default=0)

    score_for = models.IntegerField(default=0)
    score_against = models.IntegerField(default=0)

    sos_wins = models.PositiveIntegerField(default=0)
    sos_losses = models.PositiveIntegerField(default=0)
    sos_ties = models.PositiveIntegerField(default=0)

    is_final = models.BooleanField(default=False)

    def get_win_rate(self):
        if (self.wins + self.ties + self.losses) > 0:
            win_rate = (self.wins + (0.5 * self.ties)) / (self.wins + self.ties + self.losses)
        else:
            win_rate = 0

        return win_rate


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
        self.save()

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

        if self.bracket.championship.is_complete and self.bracket.loser_bracket_finals.is_complete:
            self.bracket.finalize()

        self.save()

class Bracket_4(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    n_player = models.PositiveIntegerField(default=4)
    
    championship = models.ForeignKey(
        BracketMatchup,
        on_delete=models.CASCADE,
        related_name='root',
        null=True
    )

    loser_bracket_finals = models.ForeignKey(
        BracketMatchup,
        on_delete=models.CASCADE,
        related_name='loser_root',
        null=True
    )
    
    is_active = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_losers_bracket = models.BooleanField(default=True)

    def finalize(self):
        self.is_active=False
        self.is_completed=True
        self.save()

        self.event.finalize()

    def create_matchups(self):
        championship = BracketMatchup.objects.create(
            bracket=self, event=self.event
        )
        third = BracketMatchup.objects.create(
            bracket=self, event=self.event
        )

        one_four = BracketMatchup.objects.create(
            bracket=self, 
            event=self.event,
            team_1_seed=1, 
            team_2_seed=4, 
            winner_node=championship,
            loser_node=third
        )
        two_three = BracketMatchup.objects.create(
            bracket=self,
            event=self.event,
            team_1_seed=2, 
            team_2_seed=3,
            winner_node=championship,
            loser_node=third
        )

        championship.left = one_four
        championship.right = two_three

        self.championship = championship #root
        self.save()

    def update_teams(self, playoff_teams):
        self.one_four.team_1, self.one_four.team_2 = playoff_teams[0], playoff_teams[3]
        self.two_three.team_1, self.two_three.team_2 = playoff_teams[1], playoff_teams[2]

        self.save()
        

    






