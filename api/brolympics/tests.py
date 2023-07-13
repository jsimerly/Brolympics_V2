from django.test import TestCase
from django.utils import timezone
from .models import *
from django.contrib.auth import get_user_model
import random
from unittest.mock import patch

User = get_user_model()



# Create your tests here.
class BrolympicsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='1234567890', 
            email='jon_doe@test.com',
            password='Passw0rd@123',
            first_name='John',
            last_name='Doe',
        )
        self.league = League.objects.create(
            name='Test League', 
            league_owner=self.user
        )
    
        self.brolympics = Brolympics.objects.create(
            league=self.league, 
            name='Test Brolympics',
        )
        self.team1 = Team.objects.create(brolympics=self.brolympics, name='Team 1', is_available=True)
        self.team2 = Team.objects.create(brolympics=self.brolympics, name='Team 2', is_available=False)
        self.team3 = Team.objects.create(brolympics=self.brolympics, name='Team 3', is_available=True)
        self.team4 = Team.objects.create(brolympics=self.brolympics, name='Team 4', is_available=False)

    def test_start(self):
        self.brolympics.start()
        self.assertIsNotNone(self.brolympics.start_time)
        self.assertFalse(self.brolympics.is_registration_open)
        self.assertLessEqual(self.brolympics.start_time, timezone.now())
        self.assertEqual(self.brolympics.overall_ranking.count(), 4)

    def test_get_available_teams(self):
        self.assertEqual(list(self.brolympics.get_available_teams()), [self.team1, self.team3])

    def test_is_duplicate(self):
        pairs_set = {(self.team1, self.team2)}
        self.assertTrue(self.brolympics._is_duplicate(self.team1, self.team2, pairs_set))
        self.assertTrue(self.brolympics._is_duplicate(self.team2, self.team1, pairs_set))
        self.assertFalse(self.brolympics._is_duplicate(self.team1, self.team3, pairs_set))

    def test_create_ranking_objs(self):
        self.brolympics._create_ranking_objs()
        self.assertEqual(OverallBrolympicsRanking.objects.count(), 4)
        self.assertTrue(OverallBrolympicsRanking.objects.filter(brolympics=self.brolympics, team=self.team1).exists())
        self.assertTrue(OverallBrolympicsRanking.objects.filter(brolympics=self.brolympics, team=self.team2).exists())
        self.assertTrue(OverallBrolympicsRanking.objects.filter(brolympics=self.brolympics, team=self.team3).exists())
        self.assertTrue(OverallBrolympicsRanking.objects.filter(brolympics=self.brolympics, team=self.team4).exists())

    def test_update_overall_rankings(self):
        # Placeholder for the update_overall_rankings test
        pass

class Event_H2HInitializationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='1234567890', 
            email='jon_doe@test.com',
            password='Passw0rd@123',
            first_name='John',
            last_name='Doe',
        )
        self.league = League.objects.create(
            name='Test League', 
            league_owner=self.user
        )
    
        self.brolympics = Brolympics.objects.create(
            league=self.league, 
            name='Test Brolympics',
        )
        self.teams = [Team.objects.create(brolympics=self.brolympics, name=f'Team {i+1}', is_available=(i%2==0)) for i in range(8)]
        self.h2h_event = Event_H2H.objects.create(
            brolympics=self.brolympics,
            name="test event",
            n_matches=4,
        )

    def test_create_competition_objs(self):
        self.h2h_event._create_competition_objs_h2h()
        n_teams = len(self.brolympics.teams.all())
        expected_comps = self.h2h_event.n_matches * n_teams / 2
        created_comps = len(Competition_H2H.objects.filter(event=self.h2h_event))
        self.assertEqual(expected_comps, created_comps)

    def test_create_team_pairs(self):
        pairs = self.h2h_event._create_team_pairs()

        expected_pairs = (self.h2h_event.n_matches * len(self.brolympics.teams.all()))/2
        self.assertEqual(len(pairs), expected_pairs)
        seen_pairs = set()

        team_pairs_count = {team: 0 for team in self.h2h_event.brolympics.teams.all()}
        for team1, team2 in pairs:
            team_pairs_count[team1] += 1
            team_pairs_count[team2] += 1

            pair_set = frozenset([team1, team2])
            self.assertNotIn(pair_set, seen_pairs)
            seen_pairs.add(pair_set)

        for team, count in team_pairs_count.items():
            self.assertEqual(count, self.h2h_event.n_matches)

    def test_is_comp_map_full(self):
        c_map_good = {
            't_1' : 3,
            't_2' : 3,
        }
        c_map_bad = {
            't_1' : 3,
            't_2' : 2.
        }

        self.assertTrue(self.h2h_event._is_comp_map_full(c_map_good, 3))
        self.assertFalse(self.h2h_event._is_comp_map_full(c_map_bad, 3))

    def test_create_event_ranking_h2h(self):
        self.h2h_event._create_event_ranking_h2h()
        ranking_objs = EventRanking_H2H.objects.filter(event=self.h2h_event)
        self.assertEqual(len(ranking_objs), self.brolympics.teams.count()) #2 because they were created in set up

    def test_create_bracket(self):
        self.h2h_event._create_bracket()
        self.assertIsNotNone(self.h2h_event.bracket_4)

class Event_H2HUtilityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='1234567890', 
            email='jon_doe@test.com',
            password='Passw0rd@123',
            first_name='John',
            last_name='Doe',
        )
        self.league = League.objects.create(
            name='Test League', 
            league_owner=self.user
        )
    
        self.brolympics = Brolympics.objects.create(
            league=self.league, 
            name='Test Brolympics',
        )
        self.teams = [Team.objects.create(brolympics=self.brolympics, name=f'Team {i+1}', is_available=(i%2==0)) for i in range(8)]
        self.h2h_event = Event_H2H.objects.create(
            brolympics=self.brolympics,
            name="test event",
            n_matches=4,
        )

    def test_get_completed_event_comps_h2h(self):
        for _ in range(3):
            Competition_H2H.objects.create(event=self.h2h_event, is_complete=True)

        completed_events = self.h2h_event._get_completed_event_comps_h2h()

        self.assertEqual(len(completed_events), 3)

    def test_wipe_win_loss_sos_h2h(self):
        ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[0])
        ranking.wins = 5
        ranking.losses = 3
        ranking.ties = 1
        ranking.score_for = 100
        ranking.score_against = 80
        ranking.sos_wins = 10
        ranking.sos_losses = 7
        ranking.sos_ties = 2
        ranking.save()

        self.h2h_event._wipe_win_loss_sos_h2h(ranking)

        # Assert that the values are reset to 0
        self.assertEqual(ranking.wins, 0)
        self.assertEqual(ranking.losses, 0)
        self.assertEqual(ranking.ties, 0)
        self.assertEqual(ranking.score_for, 0)
        self.assertEqual(ranking.score_against, 0)
        self.assertEqual(ranking.sos_wins, 0)
        self.assertEqual(ranking.sos_losses, 0)
        self.assertEqual(ranking.sos_ties, 0)

    def test_get_score_to_rank(self):
        score_to_rank = self.h2h_event._get_score_to_rank()
        expected_score_to_rank = {
            1: 10, 
            2: 8, 
            3: 7,  
            4: 5,  
            5: 4,  
            6: 3,  
            7: 2,  
            8: 1,
        }
        self.assertEqual(score_to_rank, expected_score_to_rank)

    def test_flatten_1(self):
        nested_list = [1, [2, 3, [4, 5]], [6, [7, 8]], 9, [10]]
        flattened_list = self.h2h_event.flatten_1(nested_list)
        expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(flattened_list, expected_list)

    def test_flatten_2(self):
        nested_list = [[1], [[2, 3], [4, 5]], [[6], [7, 8]], [9], [10]]
        flattened_list = self.h2h_event.flatten_2(nested_list)
        expected_list = [[1], [2, 3], [4, 5], [6], [7, 8], [9], [10]]
        self.assertEqual(flattened_list, expected_list)


class Event_H2HLifeCycleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='1234567890', 
            email='jon_doe@test.com',
            password='Passw0rd@123',
            first_name='John',
            last_name='Doe',
        )
        self.league = League.objects.create(
            name='Test League', 
            league_owner=self.user
        )
    
        self.brolympics = Brolympics.objects.create(
            league=self.league, 
            name='Test Brolympics',
        )
        self.teams = [Team.objects.create(brolympics=self.brolympics, name=f'Team {i+1}') for i in range(8)]
        self.h2h_event = Event_H2H.objects.create(
            brolympics=self.brolympics,
            name="test event",
            n_matches=4,
        )
        self.h2h_event.start()
    

    def test_find_available_stanard_comps(self):
        comps = self.h2h_event._find_available_standard_comps()
        self.assertEqual(len(comps), 16)

        self.teams[0].is_available = False
        self.teams[0].save()

        comps = self.h2h_event._find_available_standard_comps()
        self.assertEqual(len(comps), 12)

    def test_find_available_bracket_comps(self):
        comps = self.h2h_event._find_available_bracket_comps()
        self.assertEqual(len(comps), 0)

        self.h2h_event.bracket_4.championship.left.team_1 = self.teams[0]
        self.h2h_event.bracket_4.championship.left.team_2 = self.teams[1]
        self.h2h_event.bracket_4.championship.left.save()

        comps = self.h2h_event._find_available_bracket_comps()
        self.assertEqual(len(comps), 1)

    def test_find_available_comps_no_comps(self):
        self.h2h_event.is_round_robin_complete = False
        comps = self.h2h_event._find_available_standard_comps()
        self.assertEqual(len(comps), 16)

        self.h2h_event.is_round_robin_complete = True
        self.h2h_event.save()

        comps = self.h2h_event._find_available_bracket_comps()
        self.assertEqual(len(comps), 0)

    def test_update_event_rankings_h2h(self):
        t_1_rankings = EventRanking_H2H.objects.get(team=self.teams[0])
        t_2_rankings = EventRanking_H2H.objects.get(team=self.teams[1])
        t_3_rankings = EventRanking_H2H.objects.get(team=self.teams[2])
        t_4_rankings = EventRanking_H2H.objects.get(team=self.teams[3])

        t_1_rankings.wins = 4
        t_2_rankings.wins = 3
        t_3_rankings.wins = 2
        t_4_rankings.wins = 1

        t_1_rankings.save()
        t_2_rankings.save()
        t_3_rankings.save()
        t_4_rankings.save()

        self.h2h_event.update_event_rankings_h2h()

        rank_1 = EventRanking_H2H.objects.get(rank=1)
        rank_2 = EventRanking_H2H.objects.get(rank=2)
        rank_3 = EventRanking_H2H.objects.get(rank=3)
        rank_4 = EventRanking_H2H.objects.get(rank=4)

        t_1_rankings.refresh_from_db()
        t_2_rankings.refresh_from_db()
        t_3_rankings.refresh_from_db()
        t_4_rankings.refresh_from_db()

        self.assertEqual(rank_1, t_1_rankings)
        self.assertEqual(rank_2, t_2_rankings)
        self.assertEqual(rank_3, t_3_rankings)
        self.assertEqual(rank_4, t_4_rankings)
        self.assertEqual(10, t_1_rankings.points)
        self.assertEqual(8, t_2_rankings.points)
        self.assertEqual(7, t_3_rankings.points)
        self.assertEqual(5, t_4_rankings.points)
        pass

    def test_update_sos(self):
        team_1 = self.teams[0]
        team_2 = self.teams[1]
        team_3 = self.teams[2]

        comp_1 = Competition_H2H.objects.create(event=self.h2h_event, team_1=team_1, team_2=team_2, is_complete=True)
        comp_2 = Competition_H2H.objects.create(event=self.h2h_event, team_1=team_1, team_2=team_3, is_complete=True)

        team_2_ranking = EventRanking_H2H.objects.get(team=team_2)
        team_2_ranking.wins = 3
        team_2_ranking.losses = 1
        team_2_ranking.save()
        team_3_ranking = EventRanking_H2H.objects.get(team=team_3)
        team_3_ranking.wins = 1
        team_3_ranking.losses = 2
        team_3_ranking.ties = 1
        team_3_ranking.save()

        team_1_ranking = EventRanking_H2H.objects.get(team=team_1)

        team_rankings = [team_1_ranking, team_2_ranking, team_3_ranking]

        self.h2h_event._update_sos(team_rankings)

        self.assertEqual(team_1_ranking.sos_wins, 4)
        self.assertEqual(team_1_ranking.sos_losses, 3)
        self.assertEqual(team_1_ranking.sos_ties, 1)

    @patch('random.shuffle', lambda x: x.reverse())
    def test_break_tie(self):
        t_1_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[0], 
            wins=1, 
            losses=0, 
            ties=0
        )
        t_2_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[1], 
            wins=1, 
            losses=0, 
            ties=0
        )
        t_3_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[2], 
            wins=1, 
            losses=0, 
            ties=0
        )
        team_rankings = [t_1_ranking, t_2_ranking, t_3_ranking]
        result = self.h2h_event._break_tie(team_rankings)
        self.assertEqual(result, [t_3_ranking, t_2_ranking, t_1_ranking])

        #make t_1 1st | t_2 2nd, | t_3 3rd


        t_1_ranking.sos_wins = 3
        t_2_ranking.sos_wins = 2
        t_2_ranking.sos_ties = 2
        t_3_ranking.sos_wins = 1
        t_3_ranking.sos_losses = 3

        t_1_ranking.save()
        t_2_ranking.save()
        t_3_ranking.save()

        #Testing that SOS Wins works
        results = self.h2h_event._break_tie(team_rankings)
        self.assertEqual(results, [t_1_ranking, t_2_ranking, t_3_ranking])

        #make t_2 1st | t_1 2nd | t_3 3rd
        t_2_ranking.sos_ties = 0
        t_2_ranking.sos_wins = 4
        t_2_ranking.save()
        
        #Testing SOS works
        results = self.h2h_event._break_tie(team_rankings)
        self.assertEqual(results, [t_2_ranking, t_1_ranking, t_3_ranking])

        #make t_3 1st | t_2 2nd | t_3 3rd 
        t_1_ranking.score_for=8
        t_2_ranking.score_for=9
        t_3_ranking.score_for=10

        t_1_ranking.save()
        t_2_ranking.save()
        t_3_ranking.save()

        # Test Victory Margin Works
        results = self.h2h_event._break_tie(team_rankings)
        self.assertEqual(results, [t_3_ranking, t_2_ranking, t_1_ranking])

        #make t_1 1st | t_3 2nd | t_2 3rd
        t_1_ranking.wins = 4
        t_2_ranking.wins = 2
        t_2_ranking.losses = 2
        t_2_ranking.ties = 0
        t_3_ranking.wins = 3
        t_3_ranking.losses = 1

        t_1_ranking.save()
        t_2_ranking.save()
        t_3_ranking.save()

        #Test Won Games
        results = self.h2h_event._break_tie(team_rankings)
        self.assertEqual(results, [t_1_ranking, t_3_ranking, t_2_ranking])

        #make t_3 1st | t_2 2nd | t_1 3rd
        t_1_ranking.win_rate = .5
        t_2_ranking.win_rate = .5
        t_3_ranking.win_rate = .5 

        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[0],team_2=self.teams[1], winner=self.teams[1], is_complete=True)
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[1],team_2=self.teams[2], winner=self.teams[2], is_complete=True)
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[2],team_2=self.teams[0], winner=self.teams[2], is_complete=True)

        t_1_ranking.save()
        t_2_ranking.save()
        t_3_ranking.save()

        #Test Head to Head
        results = self.h2h_event._break_tie(team_rankings)
        self.assertEqual(results, [t_3_ranking, t_2_ranking, t_1_ranking])

    def test_tie_break_manager(self):
        # Set up team rankings with tied win rates
        t_1_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[0], wins=1, losses=0, ties=0)
        t_2_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[1], wins=1, losses=0, ties=0)
        t_3_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[2], wins=1, losses=0, ties=0)
        team_rankings = [t_1_ranking, t_2_ranking, t_3_ranking]

        # All teams have the same head to head wins, so the first tie breaker doesn't work
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[0], team_2=self.teams[1], is_complete=True, winner=self.teams[0])
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[1], team_2=self.teams[2], is_complete=True, winner=self.teams[1])
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[2], team_2=self.teams[0], is_complete=True, winner=self.teams[2])

        # Only team_1 wins an extra game, so the second tie breaker works for team_1 but not for team_2 and team_3
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[0], team_2=self.teams[1], is_complete=True, winner=self.teams[0])
        
        # team_2 has a higher margin of victory, so the third tie breaker works for team_2 over team_3
        t_2_ranking.score_for = 5
        t_2_ranking.score_against = 1
        t_2_ranking.save()

        t_3_ranking.score_for = 3
        t_3_ranking.score_against = 1
        t_3_ranking.save()

        tie_break_order = [
            self.h2h_event._break_head_to_head__wins, 
            self.h2h_event._break_won_games_total,
            self.h2h_event._break_victory_margin
        ]

        result = self.h2h_event._tie_break_manager([team_rankings], tie_break_order)
        # Assert that tie is broken
        self.assertEqual(result[0][0], t_1_ranking)  # First place: team_1
        self.assertEqual(result[1][0], t_2_ranking)  # Second place: team_2
        self.assertEqual(result[2][0], t_3_ranking)  # Third place: team_3

        ## team_2 and team_3 have the same margin of victory, so the function returns them in groups

        t_3_ranking.score_for = 5
        t_3_ranking.score_against = 1
        t_3_ranking.save()

        result = self.h2h_event._tie_break_manager([team_rankings], tie_break_order)
        self.assertEqual(len(result[0]), 1)  # First place: team_1
        self.assertEqual(len(result[1]), 2)  # Second place: team_2


    def test_get_ordered_teams(self):
        sorted_teams = [
            (self.teams[0], 3),
            (self.teams[1], 2),
            (self.teams[2], 2),
            (self.teams[3], 1),
            (self.teams[4], 3),
            (self.teams[5], 4)
        ]

        ordered_teams = self.h2h_event._get_ordered_teams(sorted_teams)

        self.assertTrue(isinstance(ordered_teams, list))
        self.assertEqual(len(ordered_teams), 4) 

        # Check that the groups are in the correct order
        self.assertEqual(ordered_teams[0][0], self.teams[5])
        self.assertEqual(ordered_teams[3][0], self.teams[3])  

        # Check that teams with the same value are in the same group
        same_value_teams = [team for team, value in sorted_teams if value == 2]
        self.assertTrue(any(team in group for group in ordered_teams for team in same_value_teams))  

    def test_is_tie_broken(self):
        tie_broken_true = [[1],[2],[3],[4]]
        tie_broken_false = [[1,2],[3],[4]]
        
        self.assertTrue(self.h2h_event._is_tie_broken(tie_broken_true))
        self.assertFalse(self.h2h_event._is_tie_broken(tie_broken_false))


    def test_group_by_win_rate_different(self):
        # create some EventRanking_H2H with the same win_rate
        same_win_rate_teams = [EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[i], win_rate=0.5) for i in range(3)]

        # create some EventRanking_H2H with different win_rate
        different_win_rate_teams = [
            EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[3], win_rate=0.6),
            EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[4], win_rate=0.4),
            EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[5], win_rate=0.8)
        ]
        all_teams = same_win_rate_teams + different_win_rate_teams

        grouped_teams = self.h2h_event._group_by_win_rate(all_teams)

        # Now, verify that the teams were grouped correctly by their win_rate
        self.assertEqual(len(grouped_teams), 4)  # there were 4 different win rates
        self.assertTrue(any(team in group for group in grouped_teams for team in same_win_rate_teams))  # the same rate teams must be in a group
        for team in different_win_rate_teams:
            self.assertTrue(any(team in group for group in grouped_teams))  # each different rate team must be in a group

    def test_group_by_win_rate_same(self):
        # create some EventRanking_H2H with the same win_rate
        same_win_rate_teams = [EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[i], win_rate=0.5) for i in range(6)]

        all_teams = same_win_rate_teams

        grouped_teams = self.h2h_event._group_by_win_rate(all_teams)

        # Now, verify that the teams were grouped correctly by their win_rate
        self.assertEqual(len(grouped_teams), 1)  # there is 1 unique win rate
        self.assertEqual(len(grouped_teams[0]), 6)  # there are 6 teams with the same win rate
        # Checking that the grouped teams are a nested list with the correct teams
        self.assertTrue(all(team in grouped_teams[0] for team in same_win_rate_teams)) 

        # Checking the structure of the grouped_teams to make sure it's a nested list
        self.assertTrue(all(isinstance(group, list) for group in grouped_teams))


    def test_break_head_to_head_wins(self):
        team_rankings = []
        for team in self.teams[0:4]:
            ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=team, wins=0, losses=0, ties=0)
            team_rankings.append(ranking)

        # Create head to head competitions, assuming all are completed
        # Team1 wins against Team2 and Team3. Team2 wins against Team3 and Team4. Team3 wins against Team4. 
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[0], team_2=self.teams[1], is_complete=True, winner=self.teams[0])
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[0], team_2=self.teams[2], is_complete=True, winner=self.teams[0])
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[1], team_2=self.teams[2], is_complete=True, winner=self.teams[1])
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[1], team_2=self.teams[3], is_complete=True, winner=self.teams[1])
        Competition_H2H.objects.create(event=self.h2h_event, team_1=self.teams[2], team_2=self.teams[3], is_complete=True, winner=self.teams[2])

        # Call the function under test
        sorted_by_head_to_head_wins = self.h2h_event._break_head_to_head__wins(team_rankings)

        # Assert the rankings are as expected
        self.assertEqual(sorted_by_head_to_head_wins[0][0], team_rankings[0])
        self.assertEqual(sorted_by_head_to_head_wins[0][1], 2) 
        self.assertEqual(sorted_by_head_to_head_wins[1][0], team_rankings[1])
        self.assertEqual(sorted_by_head_to_head_wins[1][1], 2) 
        self.assertEqual(sorted_by_head_to_head_wins[2][0], team_rankings[2])
        self.assertEqual(sorted_by_head_to_head_wins[2][1], 1) 
        self.assertEqual(sorted_by_head_to_head_wins[3][0], team_rankings[3])
        self.assertEqual(sorted_by_head_to_head_wins[3][1], 0)  

    def test_break_won_games_total(self):

        t_1_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[0], wins=2, losses=2, ties=0)
        t_2_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[1], wins=1, losses=1, ties=2)
        t_3_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[2], wins=0, losses=2, ties=4)

        team_rankings = [t_1_ranking, t_2_ranking, t_3_ranking]
        
        # Call the function under test
        sorted_by_event_wins = self.h2h_event._break_won_games_total(team_rankings)

        # Assert the rankings are as expected
        self.assertEqual(sorted_by_event_wins[0][0], t_1_ranking)
        self.assertEqual(sorted_by_event_wins[0][1], 2) 
        self.assertEqual(sorted_by_event_wins[1][0], t_2_ranking)
        self.assertEqual(sorted_by_event_wins[1][1], 1) 
        self.assertEqual(sorted_by_event_wins[2][0], t_3_ranking)
        self.assertEqual(sorted_by_event_wins[2][1], 0) 

    def test_break_victory_margin(self):

        # Create EventRanking_H2H objects with different victory margins
        t_1_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[0], score_for=10, score_against=2)
        t_2_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[1], score_for=5, score_against=1)
        t_3_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[2], score_for=6, score_against=6)

        team_rankings = [t_1_ranking, t_2_ranking, t_3_ranking]

        # Call the function under test
        sorted_by_margin_of_victory = self.h2h_event._break_victory_margin(team_rankings)

        # Assert the rankings are as expected
        self.assertEqual(sorted_by_margin_of_victory[0][0], t_1_ranking)
        self.assertEqual(sorted_by_margin_of_victory[0][1], 8)  # 10 - 2
        self.assertEqual(sorted_by_margin_of_victory[1][0], t_2_ranking)
        self.assertEqual(sorted_by_margin_of_victory[1][1], 4)  # 5 - 1
        self.assertEqual(sorted_by_margin_of_victory[2][0], t_3_ranking)
        self.assertEqual(sorted_by_margin_of_victory[2][1], 0)  # 6 - 6

    def test_break_strength_of_schedule(self):

        # Create EventRanking_H2H objects with different strength of schedules
        t_1_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[0], sos_wins=10, sos_losses=2, sos_ties=1)
        t_2_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[1], sos_wins=5, sos_losses=1, sos_ties=2)
        t_3_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[2], sos_wins=6, sos_losses=6, sos_ties=0)

        Competition_H2H.objects.create

        team_rankings = [t_1_ranking, t_2_ranking, t_3_ranking]

        # Call the function under test
        sorted_by_strength_of_schedule = self.h2h_event._break_strength_of_schedule(team_rankings)

        # Assert the rankings are as expected
        self.assertEqual(sorted_by_strength_of_schedule[0][0], t_1_ranking)
        self.assertAlmostEqual(sorted_by_strength_of_schedule[0][1], 0.807, places=2) 

        self.assertEqual(sorted_by_strength_of_schedule[1][0], t_2_ranking)
        self.assertAlmostEqual(sorted_by_strength_of_schedule[1][1], .75, places=2)  

        self.assertEqual(sorted_by_strength_of_schedule[2][0], t_3_ranking)
        self.assertAlmostEqual(sorted_by_strength_of_schedule[2][1], .5 ,places=2) 

    def test_break_strength_of_schedule_vic(self):

        # Create EventRanking_H2H objects with different strength of schedules
        t_1_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[0], sos_wins=10, sos_losses=2, sos_ties=1)
        t_2_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[1], sos_wins=5, sos_losses=1, sos_ties=2)
        t_3_ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams[2], sos_wins=6, sos_losses=6, sos_ties=0)

        Competition_H2H.objects.create

        team_rankings = [t_1_ranking, t_2_ranking, t_3_ranking]

        # Call the function under test
        sorted_by_strength_of_schedule = self.h2h_event._break_strength_of_schedule_wins(team_rankings)

        # Assert the rankings are as expected
        self.assertEqual(sorted_by_strength_of_schedule[0][0], t_1_ranking)
        self.assertEqual(sorted_by_strength_of_schedule[0][1], 10) 

        self.assertEqual(sorted_by_strength_of_schedule[1][0], t_3_ranking)
        self.assertEqual(sorted_by_strength_of_schedule[1][1], 6)  # V

        self.assertEqual(sorted_by_strength_of_schedule[2][0], t_2_ranking) #^ notice these swicthed from last time
        self.assertEqual(sorted_by_strength_of_schedule[2][1], 5)

    def test_set_rankings_and_points(self):
        t_1_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[0],
            win_rate=1.0
        )
        t_2_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[1],
            win_rate=.8333
        )
        t_3_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[2],
            win_rate=.8333
        )
        t_4_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[3],
            win_rate=.75
        )
        t_5_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[4],
            win_rate=.50
        )
        t_6_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[5],
            win_rate=0.
        )
        t_7_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[6],
            win_rate=0.0
        )
        t_8_ranking = EventRanking_H2H.objects.create(
            event=self.h2h_event, 
            team=self.teams[7],
            win_rate=0.0
        )

        team_rankings = [
            t_1_ranking, t_2_ranking, t_3_ranking, t_4_ranking, t_5_ranking,
            t_6_ranking, t_7_ranking, t_8_ranking
        ]

        expected_points_rank = {
            t_1_ranking: (10, 1),
            t_2_ranking: (8, 2),
            t_3_ranking: (7, 3),
            t_4_ranking: (5, 4),
            t_5_ranking: (4, 5),
            t_6_ranking: (2, 6),
            t_7_ranking: (2, 6),
            t_8_ranking: (2, 6)
        }

        rankings_w_points = self.h2h_event._set_rankings_and_points(team_rankings)
        for team in rankings_w_points:
            self.assertEqual(team.points, expected_points_rank[team][0])
            self.assertEqual(team.rank, expected_points_rank[team][1])

    def test_check_for_round_robin_completion(self):
        no_completed = self.h2h_event.check_for_round_robin_completion()
        self.assertFalse(no_completed)

        all_comps = self.h2h_event.competition_h2h_set.all()
        all_comps.update(is_complete=True)

        completed = self.h2h_event.check_for_round_robin_completion()
        self.assertTrue(completed)

    def test_update_bracket(self):
        rankings = self.h2h_event.event_h2h_event_rankings.all()
  
        for i, ranking in enumerate(rankings):
            ranking.rank = i+1
            ranking.save()

        self.h2h_event._update_bracket()

        self.assertEqual(self.h2h_event.bracket_4.championship.left.team_1, rankings[0].team)
        self.assertEqual(self.h2h_event.bracket_4.championship.left.team_2, rankings[3].team)
        self.assertEqual(self.h2h_event.bracket_4.championship.right.team_1, rankings[1].team)
        self.assertEqual(self.h2h_event.bracket_4.championship.right.team_2, rankings[2].team)

    #Go back up to event ranking when youre done with ties

class Event_H2HCleanUpTest(TestCase):
    pass
    #complete this once you've finished testing for other models
