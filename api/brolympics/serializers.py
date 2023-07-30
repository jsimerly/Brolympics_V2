from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

User = get_user_model()

class AllLeaguesSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    founded = serializers.SerializerMethodField()
    league_owner = serializers.SerializerMethodField()

    class Meta:
        model = League
        fields = ['uuid', 'name', 'img' ,'is_owner', 'founded', 'league_owner']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.league_owner == request.user
        return False
    
    def get_founded(self, obj):
        return str(obj.founded.year)
    
    def get_league_owner(self, obj):
        return f"{obj.league_owner.first_name} {obj.league_owner.last_name}"
    
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
    

class PlayerSerializer(serializers.ModelSerializer):
    short_name = serializers.SerializerMethodField() 
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'short_name', 'full_name', 'uuid']            

    def get_short_name(self, obj):
        return f"{obj.first_name[0]}. {obj.last_name}"
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class TeamSerializer(serializers.ModelSerializer):
    player_1 = PlayerSerializer(required=False)
    player_2 = PlayerSerializer(required=False)
    brolympics_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Team
        fields = ['name', 'player_1', 'player_2', 'is_available', 'wins', 'losses', 'ties', 'uuid', 'img', 'brolympics_uuid']

    def create(self, validated_data):
    
        player_1_uuid = validated_data.pop('player_1', None)
        player_2_uuid = validated_data.pop('player_2', None)
        img_data = validated_data.pop('img', None)
        brolympics_uuid = validated_data.pop('brolympics_uuid', None)

        brolympics = get_object_or_404(Brolympics, uuid=brolympics_uuid)

        team = Team.objects.create(brolympics=brolympics, **validated_data)

        if player_1_uuid:
            try:
                user_1 = User.objects.get(uuid=player_1_uuid)
                team.player_1 = user_1
                team.save()
            except ObjectDoesNotExist:
                pass

        if player_2_uuid:
            try:
                user_2 = User.objects.get(uuid=player_2_uuid)
                team.player_2 = user_2
                team.save()
            except ObjectDoesNotExist:
                pass 

        if img_data:
            team.img = img_data
            team.save()

        if img_data:
            team.img = img_data
            team.save()

        return team


eventAbstractFields = [ 'name', 'is_high_score_wins', 'max_score', 'min_score', 'projected_start_date', 'projected_end_date', 'is_complete', 'uuid']

def create_decimal_value(obj):
    score_type_mapping = {
        'I': 0,
        'B': -1,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        'F': 16,
    }

    return score_type_mapping.get(obj.score_type, 0)

class EventBasicSerializer_H2h(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    decimal_places = serializers.SerializerMethodField()

    class Meta:
        model = Event_H2H
        fields = [
            'n_matches', 'n_active_limit', 'n_bracket_teams', 'is_available', 'is_round_robin_complete', 'type', 'decimal_places'
            ] + eventAbstractFields

    def get_decimal_places(self, obj):
        decimal_places = create_decimal_value(obj)
        return decimal_places
    
    def get_type(self, obj):
        return 'h2h'

class EventBasicSerializer_Ind(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    decimal_places = serializers.SerializerMethodField()
    class Meta:
        model = Event_IND
        fields = [
            'display_avg_scores', 'n_competitions', 'n_active_limit', 'is_available', 'type', 'decimal_places'
            ] + eventAbstractFields
        read_only_fields = ('type',)

    def get_decimal_places(self, obj):
        decimal_places = create_decimal_value(obj)
        return decimal_places
    
    def get_type(self, obj):
        return 'ind'

class EventBasicSerializer_Team(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    decimal_places = serializers.SerializerMethodField()
    
    class Meta:
        model = Event_Team
        fields = [
            'display_avg_scores', 'n_competitions', 'n_active_limit', 'is_available', 'type', 'decimal_places'
            ] + eventAbstractFields

    def get_decimal_places(self, obj):
        decimal_places = create_decimal_value(obj)
        return decimal_places
    
    def get_type(self, obj):
        return 'team'


class BrolympicsSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    projected_start_date = serializers.SerializerMethodField()
    projected_end_date = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    team_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Brolympics
        fields = ['name', 'is_registration_open', 'projected_start_date', 'projected_end_date', 'start_time', 'end_time', 'is_complete', 'winner', 'uuid', 'img', 'teams', 'events', 'is_owner', 'is_active', 'team_uuid']

    def get_teams(self, obj):
        return TeamSerializer(obj.teams.all(), many=True, context=self.context).data

    def get_events(self, obj):
        h2h_serializer = EventBasicSerializer_H2h(obj.event_h2h_set.all(), many=True)
        ind_serializer = EventBasicSerializer_Ind(obj.event_ind_set.all(), many=True)
        team_serializer = EventBasicSerializer_Team(obj.event_team_set.all(), many=True)

        return h2h_serializer.data + ind_serializer.data + team_serializer.data
    
    def get_projected_start_date(self, obj):
        if obj.projected_start_date is not None:
            return obj.projected_start_date.strftime('%b %d, %Y')
        return None

    def get_projected_end_date(self, obj):
        if obj.projected_end_date is not None:
            return obj.projected_end_date.strftime('%b %d, %Y')
        return None
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.league.league_owner == request.user
        return False
    
    def get_team_uuid(self, obj):
        request = self.context.get('request')
        user = request.user
        team = Team.objects.filter(Q(player_1=user) | Q(player_2=user), brolympics=obj)
        if team.exists():
            return team.first().uuid
        return None

class LeagueInfoSerializer(serializers.ModelSerializer):
    founded = serializers.SerializerMethodField()
    completed_brolympics = serializers.SerializerMethodField()
    upcoming_brolympics = serializers.SerializerMethodField()

    class Meta:
        model = League
        fields = ['name', 'uuid', 'img', 'founded', 'upcoming_brolympics', 'completed_brolympics']

    def get_founded(self, obj):
        return str(obj.founded.year)
    
    def get_completed_brolympics(self, obj):
        completed = obj.brolympics_set.filter(is_complete=True)
        return BrolympicsSerializer(completed, many=True, context=self.context).data

    def get_upcoming_brolympics(self, obj):
        upcoming = obj.brolympics_set.filter(is_complete=False)
        return BrolympicsSerializer(upcoming, many=True, context=self.context).data


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
     



class TeamRankingsSerializer_H2h(serializers.ModelSerializer):
    team = TeamSerializer()
    event = serializers.SerializerMethodField()
    class Meta:
        model = EventRanking_H2H
        fields = ['event', 'team', 'rank', 'points', 'wins', 'losses', 'win_rate', 'score_for', 'score_against', 'sos_wins', 'sos_losses', 'sos_ties', 'is_final', 'uuid',]

    def get_event(self, obj):
        return obj.event.name

class TeamRankingsSerializer_Ind(serializers.ModelSerializer):
    team = TeamSerializer()
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventRanking_Ind
        fields = ['event', 'team', 'team_total_score', 'team_avg_score', 'rank', 'points', 'is_final', 'uuid']

    def get_event(self, obj):
        return obj.event.name

class TeamRankingsSerializer_Team(serializers.ModelSerializer):
    team = TeamSerializer()
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventRanking_Team
        fields = ['event', 'team', 'team_total_score', 'team_avg_score', 'rank', 'points', 'is_final', 'uuid']

    def get_event(self, obj):
        return obj.event.name



h2h_comp_fields = [
    'event', 'team_1', 'team_2', 'team_1_score', 'team_2_score',
    'winner', 'loser', 'start_time', 'end_time', 'is_complete', 'uuid', 'is_active', 'is_bracket', 'type'
]         

class BaseCompetitionSerializer(serializers.ModelSerializer):
    team_1 = TeamSerializer()
    team_2 = TeamSerializer()
    winner = TeamSerializer()
    loser = TeamSerializer()
    event = serializers.SerializerMethodField()
    is_bracket = serializers.SerializerMethodField()
    class Meta:
        model = Competition_H2H
        fields = [] + h2h_comp_fields

    def to_representation(self, instance):
        self.fields['team_1'].context.update(self.context)
        self.fields['team_2'].context.update(self.context)
        return super().to_representation(instance)
    
    def get_event(self, obj):
        return obj.event.name
    
    def get_is_bracket(self, obj):
        if isinstance(obj, BracketMatchup):
            return True
        return False



class CompetitionSerializer_H2h(BaseCompetitionSerializer):
    type = serializers.SerializerMethodField()
    class Meta(BaseCompetitionSerializer.Meta):
        fields = ['type'] + BaseCompetitionSerializer.Meta.fields

    def get_type(self, obj):
        return 'h2h'


class BracketCompetitionSerializer_H2h(BaseCompetitionSerializer):
    team_1_seed = serializers.IntegerField()
    team_2_seed = serializers.IntegerField()
    type = serializers.SerializerMethodField()

    class Meta(BaseCompetitionSerializer.Meta):
        model = BracketMatchup
        fields = ['team_1_seed', 'team_2_seed', 'type'] + BaseCompetitionSerializer.Meta.fields

    def get_type(self, obj):
        return 'bracket'
    

class CompetitionSerializer_Ind(serializers.ModelSerializer):
    team = TeamSerializer()
    event = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Competition_Ind
        fields = ['event', 'team', 'player_1_score', 'player_2_score', 'display_avg_score', 'team_score', 'avg_score', 'start_time', 'end_time', 'is_active', 'is_complete',  'uuid', 'type']

    def get_event(self, obj):
        return obj.event.name
    
    def get_type(self, obj):
        return 'ind'
    
    
class CompetitionSerializer_Team(serializers.ModelSerializer):
    team = TeamSerializer()
    event = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = Competition_Team
        fields = ['event', 'team', 'display_avg_score', 'team_score', 'start_time', 'end_time', 'is_active', 'is_complete', 'uuid', 'type']

    def get_event(self, obj):
        return obj.event.name
    
    def get_type(self, obj):
        return 'team'
    
