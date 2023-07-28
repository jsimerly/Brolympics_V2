from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from brolympics.serializers import CompetitionSerializer_H2h, CompetitionSerializer_Ind, CompetitionSerializer_Team, BracketCompetitionSerializer_H2h, PlayerSerializer

class HomeEventSerializer_H2h(serializers.ModelSerializer):
    percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = Event_H2H
        fields = ['name', 'uuid', 'percent_complete', 'start_time']

    def get_percent_complete(self, obj):
        return obj.get_percent_complete()
    
class HomeEventSerializer_Ind(serializers.ModelSerializer):
    percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = Event_IND
        fields = ['name', 'uuid', 'percent_complete', 'start_time']

    def get_percent_complete(self, obj):
        return obj.get_percent_complete()
    
class HomeEventSerializer_Team(serializers.ModelSerializer):
    percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = Event_Team
        fields = ['name', 'uuid', 'percent_complete', 'start_time']

    def get_percent_complete(self, obj):
        return obj.get_percent_complete()
    

class CompetitionMScoresSerializer_H2h(CompetitionSerializer_H2h):
    max_score = serializers.SerializerMethodField()
    min_score = serializers.SerializerMethodField()

    class Meta(CompetitionSerializer_H2h.Meta):
        fields = CompetitionSerializer_H2h.Meta.fields + ['max_score', 'min_score']

    def get_max_score(self, obj):
        return obj.event.max_score

    def get_min_score(self, obj):
        return obj.event.min_score
    
class CompetitionMScoresSerializer_Bracket(BracketCompetitionSerializer_H2h):
    max_score = serializers.SerializerMethodField()
    min_score = serializers.SerializerMethodField()

    class Meta(BracketCompetitionSerializer_H2h.Meta):
        fields = BracketCompetitionSerializer_H2h.Meta.fields + ['max_score', 'min_score']

    def get_max_score(self, obj):
        return obj.event.max_score

    def get_min_score(self, obj):
        return obj.event.min_score
    
class CompetitionMScoresSerializer_Ind(CompetitionSerializer_Ind):
    max_score = serializers.SerializerMethodField()
    min_score = serializers.SerializerMethodField()

    class Meta(CompetitionSerializer_Ind.Meta):
        fields = CompetitionSerializer_Ind.Meta.fields + ['max_score', 'min_score']

    def get_max_score(self, obj):
        return obj.event.max_score

    def get_min_score(self, obj):
        return obj.event.min_score
    
class CompetitionMScoresSerializer_Team(CompetitionSerializer_Team):
    max_score = serializers.SerializerMethodField()
    min_score = serializers.SerializerMethodField()

    class Meta(CompetitionSerializer_Team.Meta):
        fields = CompetitionSerializer_Team.Meta.fields + ['max_score', 'min_score']

    def get_max_score(self, obj):
        return obj.event.max_score

    def get_min_score(self, obj):
        return obj.event.min_score
    

class EventRankingSerializer_H2h(serializers.ModelSerializer):
    comps = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    decimal_places = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    class Meta:
        model = EventRanking_H2H
        fields = ['rank', 'points', 'wins', 'losses', 'ties', 'win_rate', 'score_for', 'score_against', 'sos_wins', 'sos_losses', 'sos_ties', 'is_final', 'comps', 'type', 'name', 'decimal_places', 'is_active']

    def get_comps(self, obj):
        comps = Competition_H2H.objects.filter(
            Q(team_1=obj.team) | Q(team_2=obj.team),
            event=obj.event
        )
        return CompetitionSerializer_H2h(comps, many=True).data
    
    def get_type(self, obj):
        return 'h2h'

    def get_name(self, obj):
        return obj.event.name

    def get_decimal_places(self,obj):
        event_dec = obj.event.score_type
        if event_dec == 'B':
            return -1
        if event_dec == 'I':
            return 0
        if event_dec == 'F':
            return 16
        return int(event_dec)
    
    def get_is_active(self, obj):
        return obj.event.is_active

class EventRankingSerializer_Ind(serializers.ModelSerializer):
    comps = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    decimal_places = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    class Meta:
        model = EventRanking_Ind
        fields = ['rank', 'points', 'is_final', 'comps', 'type', 'name', 'score', 'decimal_places', 'is_active',]

    def get_comps(self, obj):
        comps = Competition_Ind.objects.filter(team=obj.team, event=obj.event)
        return CompetitionSerializer_Ind(comps, many=True).data
    
    def get_type(self, obj):
        return 'ind'

    def get_name(self, obj):
        return obj.event.name
    
    def get_score(self, obj):
        if obj.event.display_avg_scores:
            return obj.team_avg_score
        return obj.team_total_score
    
    def get_decimal_places(self,obj):
        event_dec = obj.event.score_type
        if event_dec == 'B':
            return -1
        if event_dec == 'I':
            return 0
        if event_dec == 'F':
            return 16
        return int(event_dec)
    
    def get_is_active(self, obj):
        return obj.event.is_active


class EventRankingSerializer_Team(serializers.ModelSerializer):
    comps = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    decimal_places = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = EventRanking_Team
        fields = ['rank', 'points', 'is_final', 'comps', 'type', 'name', 'score', 'decimal_places', 'is_active', 'is_final']

    def get_comps(self, obj):
        comps = Competition_Team.objects.filter(team=obj.team, event=obj.event)
        return CompetitionSerializer_Team(comps, many=True).data
    
    def get_type(self, obj):
        return 'team'
    
    def get_name(self, obj):
        return obj.event.name
    
    def get_score(self, obj):
        if obj.event.display_avg_scores:
            return obj.team_avg_score
        return obj.team_total_score
    
    def get_decimal_places(self,obj):
        event_dec = obj.event.score_type
        if event_dec == 'B':
            return -1
        if event_dec == 'I':
            return 0
        if event_dec == 'F':
            return 16
        return int(event_dec)
    
    def get_is_active(self, obj):
        return obj.event.is_active


class OverallRankingTeamPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallBrolympicsRanking
        fields = ['rank', 'total_points', 'event_wins', 'event_podiums']
class TeamPageSerailizer(serializers.ModelSerializer):
    overall_ranking = serializers.SerializerMethodField()
    player_1 = PlayerSerializer()
    player_2 = PlayerSerializer()
    class Meta:
        model = Team
        fields = ['name', 'player_1', 'player_2', 'overall_ranking']

    def get_overall_ranking(self, obj):
        bro_rankings = obj.brolympics.overall_ranking.filter(team=obj)
        if bro_rankings.exists():
            return OverallRankingTeamPageSerializer(bro_rankings.first()).data

        return None



