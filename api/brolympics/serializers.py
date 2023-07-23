from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *

User = get_user_model()

class AllLeaguesSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    founded = serializers.SerializerMethodField()

    class Meta:
        model = League
        fields = ['uuid', 'name', 'img' ,'is_owner', 'founded']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.league_owner == request.user
        return False
    
    def get_founded(self, obj):
        return str(obj.founded.year)
    
class LeagueCreateSerializer(serializers.ModelSerializer):
    league_owner = serializers.SerializerMethodField()
    class Meta:
        model = League
        fields = ['name', 'img', 'league_owner']

    def create(self, validated_data):
        owner = validated_data.get('owner', None)
        if not owner:
            owner = self.context['request'].user
        league = League.objects.create(league_owner=owner, **validated_data)
        return league
            

class BrolympicsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brolympics
        fields = ['league', 'name', 'projected_start_date', 'img']

class EventTeamCreateAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Team
        fields = ['name', 'brolympics']

class EventIndCreateAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_IND
        fields = ['name', 'brolympics']

class EventH2HCreateAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_H2H
        fields = ['name', 'brolympics']


