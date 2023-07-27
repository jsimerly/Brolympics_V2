from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from brolympics.serializers import CompetitionSerializer_H2h, CompetitionSerializer_Ind, CompetitionSerializer_Team, BracketCompetitionSerializer_H2h

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
