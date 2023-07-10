from django.test import TestCase
from django.utils import timezone
from .models import *
from django.contrib.auth import get_user_model
import random

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

class EventTestCases_H2H(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='Jon@test.com', phone='1234567890', password='Passw0rd@123', first_name='John', last_name='Doe',)
        self.league = League.objects.create(name='Test League', league_owner=self.user)
    
        self.brolympics = Brolympics.objects.create(league=self.league, name='Test Brolympics')
        self.team_a = Team.objects.create(brolympics=self.brolympics, name='Team A', is_available=True)
        self.team_b = Team.objects.create(brolympics=self.brolympics, name='Team B', is_available=False)
        self.team_c = Team.objects.create(brolympics=self.brolympics, name='Team C', is_available=True)
        self.team_d = Team.objects.create(brolympics=self.brolympics, name='Team D', is_available=False)
        self.team_e = Team.objects.create(brolympics=self.brolympics, name='Team E', is_available=True)
        self.team_f = Team.objects.create(brolympics=self.brolympics, name='Team F', is_available=False)
        self.team_g = Team.objects.create(brolympics=self.brolympics, name='Team G', is_available=True)
        self.team_h = Team.objects.create(brolympics=self.brolympics, name='Team H', is_available=False)

        self.player_a1 = User.objects.create_user(phone='1234567890', password='Passw0rd@123', first_name='A', last_name='1', email='a1@test.com')
        self.player_a2 = User.objects.create_user(phone='1234567891', password='Passw0rd@123', first_name='A', last_name='2', email='a2@test.com')
        self.player_b1 = User.objects.create_user(phone='1234567892', password='Passw0rd@123', first_name='B', last_name='1', email='b1@test.com')
        self.player_b2 = User.objects.create_user(phone='1234567893', password='Passw0rd@123', first_name='B', last_name='2', email='b2@test.com')
        self.player_c1 = User.objects.create_user(phone='1234567894', password='Passw0rd@123', first_name='C', last_name='1', email='c1@test.com')
        self.player_c2 = User.objects.create_user(phone='1234567895', password='Passw0rd@123', first_name='C', last_name='2', email='c2@test.com')
        self.player_d1 = User.objects.create_user(phone='1234567896', password='Passw0rd@123', first_name='D', last_name='1', email='d1@test.com')
        self.player_d2 = User.objects.create_user(phone='1234567897', password='Passw0rd@123', first_name='D', last_name='2', email='d2@test.com')
        self.player_e1 = User.objects.create_user(phone='1234567898', password='Passw0rd@123', first_name='E', last_name='1', email='e1@test.com')
        self.player_e2 = User.objects.create_user(phone='1234567899', password='Passw0rd@123', first_name='E', last_name='2', email='e2@test.com')
        self.player_f1 = User.objects.create_user(phone='1234567812', password='Passw0rd@123', first_name='F', last_name='1', email='f1@test.com')
        self.player_f2 = User.objects.create_user(phone='1234567813', password='Passw0rd@123', first_name='F', last_name='2', email='f2@test.com')
        self.player_g1 = User.objects.create_user(phone='1234567814', password='Passw0rd@123', first_name='G', last_name='1', email='g1@test.com')
        self.player_g2 = User.objects.create_user(phone='1234567815', password='Passw0rd@123', first_name='G', last_name='2', email='g2@test.com')
        self.player_h1 = User.objects.create_user(phone='1234567816', password='Passw0rd@123', first_name='H', last_name='1', email='h1@test.com')
        self.player_h2 = User.objects.create_user(phone='1234567817', password='Passw0rd@123', first_name='H', last_name='2', email='h2@test.com')

        self.team_a.player_1, self.team_a.player_2 = self.player_a1, self.player_a2
        self.team_b.player_1, self.team_b.player_2 = self.player_b1, self.player_b2
        self.team_c.player_1, self.team_c.player_2 = self.player_c1, self.player_c2
        self.team_d.player_1, self.team_d.player_2 = self.player_d1, self.player_d2
        self.team_e.player_1, self.team_e.player_2 = self.player_e1, self.player_e2
        self.team_f.player_1, self.team_f.player_2 = self.player_f1, self.player_f2
        self.team_g.player_1, self.team_g.player_2 = self.player_g1, self.player_g2
        self.team_h.player_1, self.team_h.player_2 = self.player_h1, self.player_h2

        self.teams_list = [self.team_a, self.team_b, self.team_c, self.team_d, self.team_e, self.team_f, self.team_g, self.team_h]

        self.h2h_event = Event.objects.create(
            brolympics=self.brolympics,
            name='Test H2H Event',
            type='H',
            n_matches=4,
            n_active_limit=1,
        )

        self.event_rankings = [
            EventRanking_H2H.objects.create(event=self.h2h_event, team=self.teams_list[i])
            for i in range(len(self.teams_list))
        ]

    # Functions # 
    def simulate_h2h_matchup(self, comp):
        comp.start()
        win_score = comp.event.max_score
        lose_score = random.randint(comp.event.min_score, comp.event.max_score-1)
        
        scores = [win_score, lose_score]
        random.shuffle(scores)

        comp.end(scores[0], scores[1])


    # GENERAL TESTING #

    ## HEAD TO HEAD UNIT TESTING ##
    def test_is_comp_map_full(self):
        comp_map = {self.team_a: 4, self.team_b: 4, self.team_c: 4}
        self.assertTrue(self.h2h_event._is_comp_map_full(comp_map, 4))
        comp_map[self.team_c] = 3
        self.assertFalse(self.h2h_event._is_comp_map_full(comp_map, 4))

    def test_create_team_pairs(self):
        pairs = self.h2h_event.create_team_pairs()

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
    

    def test_create_competition_objs_h2h(self):
        self.h2h_event.create_competition_objs_h2h()
        pairs = self.h2h_event.create_team_pairs()
        competitions = Competition_H2H.objects.filter(event=self.h2h_event)
        self.assertEqual(len(pairs), competitions.count())

    def test_create_event_ranking_h2h(self):
        self.h2h_event.create_event_ranking_h2h()
        ranking_objs = EventRanking_H2H.objects.filter(event=self.h2h_event)
        self.assertEqual(len(ranking_objs), self.brolympics.teams.count()*2) #2 because they were created in set up

    def test_create_bracket(self):
        self.h2h_event.create_bracket()
        self.assertIsNotNone(self.h2h_event.bracket_4)

    def test_get_completed_event_comps_h2h(self):
        self.h2h_event.create_competition_objs_h2h()
        competitions = Competition_H2H.objects.filter(event=self.h2h_event)
        
        for i in range(3):
            self.simulate_h2h_matchup(competitions[i])

        completed_events = self.h2h_event._get_completed_event_comps_h2h()

        self.assertEqual(len(completed_events), 3)

    def test_wipe_win_loss_sos_h2h(self):
        ranking = EventRanking_H2H.objects.create(event=self.h2h_event, team=self.team_a)
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

    def test_group_by_win_rate(self):
        team_a_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_a)
        team_b_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_b)
        team_c_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_c)

        team_a_ranking.win_rate = 1
        team_b_ranking.win_rate = .5
        team_c_ranking.win_rate = 1

        team_a_ranking.save()
        team_b_ranking.save()
        team_c_ranking.save()


        two_teams = [team_a_ranking, team_b_ranking, team_c_ranking]
        
        grouped_by_win_rate = self.h2h_event._group_by_win_rate(two_teams)
        self.assertEqual(grouped_by_win_rate, [[team_a_ranking, team_c_ranking], [team_b_ranking]])

        team_c_ranking.win_rate = 0
        team_c_ranking.save()

        grouped_by_win_rate = self.h2h_event._group_by_win_rate(two_teams)
        self.assertEqual(grouped_by_win_rate, [[team_a_ranking], [team_b_ranking], [team_c_ranking]])



    def test_update_event_ranking_h2h(self):
        comp_1 = Competition_H2H.objects.create(event=self.h2h_event, team_1=self.team_a, team_2=self.team_b)
        comp_2 = Competition_H2H.objects.create(event=self.h2h_event, team_1=self.team_a, team_2=self.team_c)
        comp_3 = Competition_H2H.objects.create(event=self.h2h_event, team_1=self.team_c, team_2=self.team_b)
        comp_4 = Competition_H2H.objects.create(event=self.h2h_event, team_1=self.team_a, team_2=self.team_d)
        comp_5 = Competition_H2H.objects.create(event=self.h2h_event, team_1=self.team_d, team_2=self.team_e)

        comp_1.end(10,9) # a > b
        comp_2.end(10,9) # a > c
        comp_3.end(10,9) # c > b
        comp_4.end(10,9) # a > d
        comp_5.end(10,8) # d > e || test tie breaker between d and c (d should win)

        team_a_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_a)
        team_b_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_b)
        team_c_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_c)
        team_d_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_d)
        team_e_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_e)

        self.assertEqual(team_a_ranking.wins, 3)
        self.assertEqual(team_a_ranking.losses, 0)
        self.assertEqual(team_a_ranking.score_for, 30)
        self.assertEqual(team_a_ranking.score_against, 27)
        self.assertEqual(team_a_ranking.rank, 1)
        

        self.assertEqual(team_b_ranking.wins, 0)
        self.assertEqual(team_b_ranking.losses, 2)
        self.assertEqual(team_b_ranking.score_for, 18)
        self.assertEqual(team_b_ranking.score_against, 20)
        

        self.assertEqual(team_c_ranking.wins, 1)
        self.assertEqual(team_c_ranking.losses, 1)
        self.assertEqual(team_c_ranking.score_for, 19)
        self.assertEqual(team_c_ranking.score_against, 19)
        self.assertEqual(team_c_ranking.rank, 3)

        self.assertEqual(team_d_ranking.wins, 1)
        self.assertEqual(team_d_ranking.losses, 1)
        self.assertEqual(team_d_ranking.score_for, 19)
        self.assertEqual(team_d_ranking.score_against, 18)
        self.assertEqual(team_d_ranking.rank, 2)

        self.assertEqual(team_e_ranking.wins, 0)
        self.assertEqual(team_e_ranking.losses, 1)
        self.assertEqual(team_e_ranking.score_for, 8)
        self.assertEqual(team_e_ranking.score_against, 10)

    def test_update_ranking_score_and_sos_h2h(self):
        team1_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_a)
        team2_ranking = EventRanking_H2H.objects.get(event=self.h2h_event, team=self.team_b)


        comp = Competition_H2H.objects.create(event=self.h2h_event, team_1=self.team_a, team_2=self.team_b)

        comp.end(5,4)

        team_rankings = EventRanking_H2H.objects.all()
        self.h2h_event._update_ranking_score_and_sos_h2h(comp, team_rankings)

        team1_ranking = EventRanking_H2H.objects.get(team=self.team_a)
        team2_ranking = EventRanking_H2H.objects.get(team=self.team_b)

        self.assertEqual(team1_ranking.wins, 1)
        self.assertEqual(team1_ranking.score_for, 5)
        self.assertEqual(team1_ranking.score_against, 4)

        self.assertEqual(team2_ranking.losses, 1)
        self.assertEqual(team2_ranking.score_for, 4)
        self.assertEqual(team2_ranking.score_against, 5)



    def test_update_event_rankings_h2h(self):
        self.h2h_event.start()
        self.h2h_event.update_event_rankings_h2h()


class TestUpdateEventRankingsH2H(TestCase):
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
        self.players = [
            User.objects.create(
                phone=f'123456789{i}', 
                email=f'jon_doe{i}@test.com',
                password='Passw0rd@123',
                first_name=f'John {i}',
                last_name='Doe',
            )
            for i in range(1,16)
        ]
        self.teams = [
            Team.objects.create(
                name=f"team{i}", 
                brolympics=self.brolympics,
                player_1=self.players[i],
                player_2=self.players[i*2]
            ) 
            for i in range(1, 8)
        ]
        self.h2h_event = Event.objects.create(
            brolympics=self.brolympics,
            name='Test H2H Event',
            type='H',
            n_matches=4,
            n_active_limit=1,
        )
        
        # Start the event
        self.h2h_event.start()





