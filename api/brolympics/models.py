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

    total_score = models.FloatField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)


class EventAbstactBase(models.Model):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )

    name = models.CharField(max_length=60)

    is_high_score_wins = models.BooleanField(default=True)
    max_score = models.FloatField(default=100)
    min_score = models.FloatField(default=0)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_concluded = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def start(self):
        self.start_time = timezone.now()
        self.is_available = True
        self.create_child_objects()

    def _get_score_to_rank(self):
        n_teams = len(self.brolympics.teams.all())
        score_map = {
            1 : n_teams+2,
            2 : n_teams,
            3 : n_teams-1,
        }

        for i in range(3, n_teams):
            score_map[i+1] = n_teams-i

        return score_map

    def finalize(self):
        self.end_time = timezone.now()
        self.is_concluded = True
        self.finalized_rankings()
        

class Event_IND(EventAbstactBase):
    is_individual_scores = models.BooleanField(default=True)
    
    n_competitions = models.PositiveIntegerField(default=1)

    n_active_limit = models.PositiveIntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=False)

    ## Initialization

    def create_child_objects(self):
        self._create_competition_and_ranking_objs_ind()

    def _create_competition_and_ranking_objs_ind(self):
        competitions = []
        rankings = []
        for team in self.brolympics:
            for _ in range(self.n_competitions):
                competitions.append(Competition_Ind(event=self, team=team))
            rankings.append(EventRanking_Ind(event=self, team=team, is_individual_scores=self.is_individual_scores))

        Competition_Ind.objects.bulk_create(competitions)
        EventRanking_Ind.objects.bulk_create(rankings)
   
    ## End of Initialization ##

    ## Event Utility ##
    def full_update_event_rankings_ind(self):
        team_rankings = list(self.event_ind_event_rankings.all())
        for ranking in team_rankings:
            self._wipe_rankings(ranking)
        pass

    def _get_completed_event_comps_ind(self):
        return Competition_Ind.objects.filter(
            event=self,
            is_complete=True
        )
    
    def _wipe_rankings(self, rankings):
        rankings.update(
            player_1_total_score=0,
            player_1_avg_score=0,
            player_2_total_score=0,
            player_2_avg_score=0,
            team_total_score=0,
            team_avg_score=0,
            rank=0,
            points=0,
        )


        pass

    ## End of Event Utility

    ## Event Life Cycle ##
    def is_event_available(self):
        # Return true or false, it true then 
        pass

    def update_event_rankings_h2h(self):
        pass

    def _group_by_score(self):
        pass

    def check_for_completion(self):
        pass

    ## End of Life Cycle

    ## Event Clean Up ##
    def finalize_rankings(self):
        pass

    def _set_event_rankings_final(self):
        pass




    
    



    




    ## End of Life Cylce ##



    def _finalize_rankings():
        pass


class Event_H2H(EventAbstactBase):
    brolympics = models.ForeignKey(
        Brolympics,
        on_delete=models.CASCADE,
        related_name='events'
    )

    #add validation that it's an even number and no more than n_teams-1
    n_matches = models.PositiveIntegerField(null=False, blank=False)
    n_active_limit = models.PositiveIntegerField(blank=True, null=True)
    n_bracket_teams = models.PositiveIntegerField(default=4)

    is_available = models.BooleanField(default=False)
    is_round_robin_complete = models.BooleanField(default=False)


    ## Initialization ## 
    def create_child_objects(self):   #used by parent for start()
        self._create_competition_objs_h2h()
        self._create_event_ranking_h2h()
        self._create_bracket()

    def _create_competition_objs_h2h(self):
        pairs = self._create_team_pairs()
        competitions = [
            Competition_H2H(event=self, team_1=pair[0], team_2=pair[1])
            for pair in pairs
        ]
        Competition_H2H.objects.bulk_create(competitions)

    def _create_team_pairs(self):
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
            
    def _is_comp_map_full(self, comp_map, target_n):
        if not comp_map:
            return False
        
        for value in comp_map.values():
            if value != target_n:
                return False
        return True 

    def _create_event_ranking_h2h(self):
        ranking_objs = [
            EventRanking_H2H(event=self, team=team)
            for team in self.brolympics.teams.all()
        ]
        EventRanking_H2H.objects.bulk_create(ranking_objs)

    def _create_bracket(self):
        bracket_obj = Bracket_4.objects.create(event=self)
        bracket_obj.create_matchups()



    ## End of Initialization ##

    ## Utility ## 
    def full_update_event_rankings_h2h(self):
        team_rankings = list(self.event_h2h_event_rankings.all())

        self._wipe_win_loss_sos_h2h(team_rankings)
        
        #need a loop through and updated wins
        self._update_sos(team_rankings)
       

    def _get_completed_event_comps_h2h(self):
        return Competition_H2H.objects.filter(
            event=self,
            is_complete=True,
        )

    def _wipe_win_loss_sos_h2h(self, rankings):
        rankings.update(
            wins = 0,
            losses = 0,
            ties = 0,
            score_for = 0,
            score_against = 0,
            sos_wins = 0,
            sos_losses = 0,
            sos_ties = 0,
        )

    
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

    ## End of Utility ## 

    ## Event Life Cycle ##
    def find_available_comps(self):
        if self.is_round_robin_complete:
            return self._find_available_standard_comps()
        return self._find_available_bracket_comps()
    
    def _find_available_standard_comps(self):
        return Competition_H2H.objects.filter(
            event=self,
            team_1__is_available=True,
            team_2__is_available=True,
        )   
    
    def _find_available_bracket_comps(self):
        return BracketMatchup.objects.filter(
            bracket=self.bracket_4,
            team_1__isnull=False,
            team_2__isnull=False,
            is_complete=False
        )
    
        #Comp start and end here #
    
    def update_event_rankings_h2h(self, team_rankings=None):
        if team_rankings == None:
            team_rankings = list(self.event_h2h_event_rankings.all())
        team_rankings = sorted(team_rankings, key=lambda x: x.win_rate, reverse=True)

        self._update_sos(team_rankings)
        tie_broken_teams = self._break_tie(team_rankings)
        self._set_rankings_and_points(tie_broken_teams)

        update_fields = ['rank', 'points']
        EventRanking_H2H.objects.bulk_update(team_rankings, update_fields)
        

    def _update_sos(self, team_rankings):
        team_to_wlt = {
            team_ranking.team: {
                'wins': team_ranking.wins,
                'losses': team_ranking.losses,
                'ties': team_ranking.ties,
            } 
            for team_ranking in team_rankings
        }

        for team_ranking in team_rankings:
            team = team_ranking.team
            team_completed_competitions = Competition_H2H.objects.filter(
                Q(team_1=team) | Q(team_2=team), 
                event=self, 
                is_complete=True
            )

            for comp in team_completed_competitions:
                if comp.team_1 == team:
                    opponent = comp.team_2
                else:
                    opponent = comp.team_1

                team_ranking.sos_wins += team_to_wlt[opponent]['wins']
                team_ranking.sos_losses += team_to_wlt[opponent]['losses']
                team_ranking.sos_ties += team_to_wlt[opponent]['ties']

            team_ranking.save()


    def _break_tie(self, team_rankings):
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
    
    def _tie_break_manager(self, tied_teams, tie_break_order_funcs):
        
        for tie_breaker in tie_break_order_funcs:
            doubley_nested_teams = []
            for group in tied_teams:
                nested_group = tie_breaker(group)
                doubley_nested_teams.append(nested_group)

            ordered_doubley_nested = []
            for nested_group in doubley_nested_teams:
                ordered_group = self._get_ordered_teams(nested_group)
                ordered_doubley_nested.append(ordered_group)

            tied_teams = self.flatten_2(ordered_doubley_nested)
            
            if self._is_tie_broken(tied_teams):
                break

        return tied_teams
    
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

    def _is_tie_broken(self, tied_teams):
        for group in tied_teams:
            if len(group) != 1:
                return False
        return True
    
    def _group_by_win_rate(self, teams):
        win_rate_to_teams = {}

        for team in teams:
            win_rate = team.win_rate
            if win_rate not in win_rate_to_teams:
                win_rate_to_teams[win_rate] = []
            win_rate_to_teams[win_rate].append(team)

        return list(win_rate_to_teams.values())
    
    def _break_head_to_head__wins(self, teams):
        tied_team_ids = [team.team.id for team in teams]
        
        head_to_head_comps = Competition_H2H.objects.filter(
            event=self,
            is_complete=True,
            team_1__in=tied_team_ids,
            team_2__in=tied_team_ids
        )

        team_h2h_wins_map = {team: 0 for team in teams}
        for comp in head_to_head_comps:
            for team in teams:
                if comp.winner == team.team:
                    team_h2h_wins_map[team] += 1

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
                strength_of_schedule[team] = (team.sos_wins + (team.sos_ties * 0.5)) / (team.sos_wins + team.sos_losses + team.sos_ties)
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
    
    def _set_rankings_and_points(self, team_rankings):
        score_map = self._get_score_to_rank()

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
                    split_points = tied_teams_points/len(tied_teams)
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

        return team_rankings

    def check_for_round_robin_completion(self):
        if self.start_time == None or self.is_round_robin_complete:
            return None
        
        uncompleted = Competition_H2H.objects.filter(event=self, is_complete=False)
        if len(uncompleted) == 0:
            self.is_round_robin_complete = True
            self._update_bracket()
            self.save()

            return True
        return False
        

    def _update_bracket(self):
        top_4_rankings = self.event_h2h_event_rankings.all().order_by('rank')[:self.n_bracket_teams]
        self.bracket_4.update_teams(top_4_rankings)
        
    ## End of Life Cycle ##

    ## Event Clean Up ##
    def finalize_rankings(self): #used by parent for finalize()
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
        self._set_event_rankings_final()

    def _set_event_rankings_final(self):
        self.event_h2h_event_rankings.all().update(is_final=True)

    ## End of Event Clean Up
                    

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

    is_available = models.BooleanField(default=True)

    score = models.FloatField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

class Competition_Ind(models.Model):
    event = models.ForeignKey(
        Event_IND,
        on_delete=models.CASCADE,
        related_name='ind_comp',
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='ind_competition_team',
    )

    player_1_score = models.FloatField(blank=True, null=True)
    player_2_score = models.FloatField(blank=True, null=True)

    team_score = models.FloatField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)


class Competition_H2H_Base(models.Model):
    event = models.ForeignKey(
        Event_H2H,
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )

    team_1 = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_comp_team_1',
        null=True, # allowed to be null because this is also used in bracket
        blank=True
    )

    team_2 = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_comp_team_2',
        null=True,
        blank=True
    )

    team_1_score = models.FloatField(blank=True, null=True)
    team_2_score = models.FloatField(blank=True, null=True)

    winner = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_comp_wins',
        null=True,
        blank=True,
        default=None
    )
    loser = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='%(class)s_comp_losses',
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
        Event_IND,
        on_delete=models.CASCADE,
        related_name='event_ind_event_rankings'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='team_ind_event_rankings'
    )

    is_individual_scores = models.BooleanField(default=True)

    player_1_total_score = models.FloatField(blank=True, null=True)
    player_1_avg_score = models.FloatField(blank=True, null=True)
    player_2_total_score = models.FloatField(blank=True, null=True)
    player_2_avg_score = models.FloatField(blank=True, null=True)
    
    team_total_score = models.FloatField(blank=True, null=True)
    team_avg_score = models.FloatField(blank=True, null=True)
    
    rank = models.PositiveIntegerField(default=1)
    points = models.FloatField(default=0)

    is_final = models.BooleanField(default=False)

class EventRanking_H2H(models.Model):
    event = models.ForeignKey(
        Event_H2H,
        on_delete=models.CASCADE,
        related_name='event_h2h_event_rankings'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='team_h2h_event_rankings'
    )

    rank = models.PositiveIntegerField(default=1)
    points = models.FloatField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    win_rate = models.FloatField(default=0)

    score_for = models.FloatField(default=0)
    score_against = models.FloatField(default=0)

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
    event = models.OneToOneField(Event_H2H, on_delete=models.CASCADE)

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
    is_complete = models.BooleanField(default=False)
    is_losers_bracket = models.BooleanField(default=True)

    def finalize(self):
        self.is_active=False
        self.is_complete=True
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
        seed_1 = playoff_teams[0].team
        seed_2 = playoff_teams[1].team
        seed_3 = playoff_teams[2].team
        seed_4 = playoff_teams[3].team

        self.championship.left.team_1 = seed_1
        self.championship.left.team_2 = seed_4

        self.championship.right.team_1 = seed_2
        self.championship.right.team_2 = seed_3

        self.save()
        

    






