from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *

User = get_user_model()

class UserForLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']

class LeagueSerializer(serializers.ModelSerializer):
    league_owner = UserForLeagueSerializer()

    class Meta:
        model = League
        fields = ['name', 'league_owner', 'founded']

class BrolympicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brolympics
        fields = ['n_teams', 'started', 'ended', 'completed', 'winner']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'type', 'high_score_wins', 'max_score', 'min_score', 'n_active_limit', 'concluded']

class OverallBrolympicRankngsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallBrolympicsRanking
        fields = ['ranking', 'team', 'total_score', 'win_rate']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'team_picture', 'player_1', 'player_2', 'score', 'wins', 'losses', 'ties']

class IndividualCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualCompetition
        fields = ['team', 'player_1_score', 'player_2_score', 'active', 'complete']

class H2hCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = H2hCompetition
        field = ['team_1', 'team_2', 'team_1_score', 'team_2_score', 'active', 'complete']    

class EventRanking_IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRanking_Individual
        fields = ['ranking', 'earned_points', 'team_score', 'final']

class EventRanking_H2hSerializer(serializers.ModelSerializer):
    class Meta:
        models = EventRanking_H2H
        fields = ['ranking', 'earned_poitns', 'wins', 'losses', 'ties', 'final']


