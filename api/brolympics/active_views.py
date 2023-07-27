from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from datetime import datetime
from brolympics.models import *
from brolympics.serializers import *
from brolympics.active_serializers import *
import base64
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q


class StartBrolympics(APIView):
    def get_object(self, uuid):
        brolympics = get_object_or_404(Brolympics, uuid=uuid)

        if self.request.user != brolympics.league.league_owner:
            raise PermissionDenied('You do not have permission to start this Brolympcs.')
        
        return brolympics

        
    def put(self, request):
        uuid = request.data.get('uuid')
        brolympics = self.get_object(uuid)

        brolympics.start()
        return Response(status=status.HTTP_200_OK)
    
class StartEvents(APIView):
    def confirm(self, event):
        if self.request.user != event.brolympics.league.league_owner:
            raise PermissionDenied('You do not have permission to start this event.')
        
        if event.is_active:
            raise ValueError('This event is already active.')
        
    def put(self, request):
        event_uuid = request.data.get('uuid')
        event_type = request.data.get('type')

        if event_type == 'h2h':
            event = get_object_or_404(Event_H2H, uuid=event_uuid)
            self.confirm(event)

            event.start()
            return Response(status=status.HTTP_200_OK)

        elif event_type == 'ind':
            event = get_object_or_404(Event_IND, uuid=event_uuid)
            self.confirm(event)

            event.start()
            return Response(status=status.HTTP_200_OK)

        elif event_type == 'team':
            event = get_object_or_404(Event_Team, uuid=event_uuid)
            self.confirm(event)

            event.start()
            return Response(status=status.HTTP_200_OK)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UnstartedEvents(APIView):
    def get(self, request, uuid):
        brolympics = get_object_or_404(Brolympics, uuid=uuid)
        all_events = brolympics.get_all_events()

        h2h = all_events['h2h'].filter(is_active=False, is_complete=False)
        ind = all_events['ind'].filter(is_active=False, is_complete=False)
        team = all_events['team'].filter(is_active=False, is_complete=False)

        h2h_serializer = EventBasicSerializer_H2h(h2h, many=True)
        ind_serializer = EventBasicSerializer_Ind(ind, many=True) 
        team_serializer = EventBasicSerializer_Team(team, many=True)

        serializers = h2h_serializer.data + ind_serializer.data + team_serializer.data

        return Response(serializers, status=status.HTTP_200_OK)
    

class GetActiveHome(APIView):
    def get_object(self, uuid):
        brolympics = get_object_or_404(Brolympics, uuid=uuid)
        return brolympics
    
    def get_available(self, qset):
        available = [
            event.find_available_comps(self.request.user)
            for event in qset
        ]
        return available
    
    def get_active(self, qset):
        active = [
            event.find_active_comps()
            for event in qset
        ]
        return active

    def get(self, request, uuid):
        brolympics = self.get_object(uuid)  
        event_map = brolympics.get_active_events()

        # Active Events
        h2h = event_map['h2h']
        ind = event_map['ind']
        team = event_map['team']

        h2h_event_serialized = HomeEventSerializer_H2h(
            h2h, 
            many=True, 
            ).data
        ind_event_serialized = HomeEventSerializer_Ind(
            ind, 
            many=True
            ).data
        team_event_serialized = HomeEventSerializer_Team(
            team, 
            many=True
            ).data

        all_serialized = h2h_event_serialized + ind_event_serialized + team_event_serialized
        all_serialized.sort(key=lambda x: x['start_time'] if x['start_time'] is not None else datetime.max, reverse=False)

        #Available_competitions
        h2h_available = {'std':[], 'bracket':[]}
        for event in h2h:
            comps = event.find_available_comps(request.user)
            h2h_available['std'].extend(comps['std'])
            h2h_available['bracket'].extend(comps['bracket'])
        
        ind_available = self.get_available(ind)
        team_available = self.get_available(team)
        
        h2h_comp_serialized = CompetitionSerializer_H2h(
            h2h_available['std'], 
            many=True,
            context={'request': request}
            ).data 
        
        h2h_bracket_serialized = BracketCompetitionSerializer_H2h(
            h2h_available['bracket'], 
            many=True,
            context={'request': request}
            ).data 

        ind_comp_serialized = [
            CompetitionSerializer_Ind(comp, many=True, context={'request': request}).data 
            for comp in ind_available
        ]
        team_comp_serializerd = [
            CompetitionSerializer_Team(comp, many=True, context={'request': request}).data 
            for comp in team_available
        ]
        available_comps = h2h_comp_serialized + ind_comp_serialized + team_comp_serializerd

        #Active
        h2h_active = {'std': [], 'bracket':[]}
        for event in h2h:
            comps = event.find_active_comps()
            h2h_active['std'].extend(comps['std'])
            h2h_active['bracket'].extend(comps['bracket'])

        ind_active = self.get_active(ind)
        team_active = self.get_active(team)

        bracket_active_serialized = BracketCompetitionSerializer_H2h(
            h2h_active['bracket'], 
            many=True,
            context={'request': request}
            ).data
        h2h_active_serialized = CompetitionSerializer_H2h(
            h2h_active['std'], 
            many=True,
            context={'request': request}
            ).data
        ind_active_serialized = CompetitionSerializer_H2h(
            ind_active, 
            many=True,
            context={'request': request}
            ).data
        team_active_serialized = CompetitionSerializer_Team(
            team_active, 
            many=True,
            context={'request': request}
            ).data 

        all_active_data = h2h_active_serialized + ind_active_serialized + team_active_serialized
       
        data = {
            'active_events' : all_serialized,
            'available_competitions' : available_comps,
            'available_bracket_comps' : h2h_bracket_serialized,
            'active_bracket_comps' : bracket_active_serialized,
            'active_competitions' : all_active_data,
        }

        return Response(data ,status=status.HTTP_200_OK)
    
class StartCompetition(APIView):
    def get_object(self, comp_uuid, comp_type):
        if comp_type == 'h2h':
            comp = get_object_or_404(Competition_H2H, uuid=comp_uuid)
            return comp
        if comp_type == 'bracket':
            comp = get_object_or_404(BracketMatchup, uuid=comp_uuid)
            return comp

        if comp_type == 'ind':
            comp = get_object_or_404(Competition_Ind, uuid=comp_uuid)
            return comp
        
        if comp_type == 'team':
            comp = get_object_or_404(Competition_Team, uuid=comp_uuid)
            return comp

        raise ValueError('Cannot match the competition type.')


    def confirm(self, comp):        
        if comp.is_active:
            raise ValueError('This comp is already active.')
        
    def put(self, request):
        print(request.data)
        comp_uuid = request.data.get('uuid')
        comp_type = request.data.get('type')

        print(comp_uuid)
        print(comp_type)

        comp = self.get_object(comp_uuid, comp_type)
        comp.start()

        return Response({'comp_uuid': comp_uuid}, status=status.HTTP_200_OK)
    
class IsInCompetition(APIView):
    def find_comp(self, user):
        h2h = Competition_H2H.objects.filter(
            Q(team_1__player_1=user) | Q(team_1__player_2=user) | 
            Q(team_2__player_1=user) | Q(team_2__player_2=user),
            is_active=True,
        )
        if h2h.exists():
            return h2h.first(), 'h2h'

        bracket = BracketMatchup.objects.filter(
            Q(team_1__player_1=user) | Q(team_1__player_2=user) | 
            Q(team_2__player_1=user) | Q(team_2__player_2=user),
            is_active=True,
        )
        if bracket.exists():
            return bracket.first(), 'h2h'

        ind = Competition_Ind.objects.filter(
            Q(team__player_1=user) | Q(team__player_2=user),
            is_active=True,
        )
        if ind.exists():
            return ind.first(), 'ind'

        team = Competition_Team.objects.filter(
            Q(team__player_1=user) | Q(team__player_2=user),
            is_active=True,
        )
        if team.exists():
            return team.first(), 'team'
        
        user.is_available = True
        user.save()
        raise ValueError('No Competition currently exists')



    def get(self, request):
        user = request.user
        data = {
            'is_available' : True,
            'comp_uuid' : ''
        }
        if not user.is_available:
            comp, type = self.find_comp(user)
            data = {
                'is_available' : False,
                'comp_uuid' : comp.uuid,
                'type': type
            }

        return Response(data, status=status.HTTP_200_OK)
    
class GetCompH2h(APIView):
    def get(self, request, uuid):
        h2h_comp_qset = Competition_H2H.objects.filter(uuid=uuid)

        if h2h_comp_qset.exists():
            comp = h2h_comp_qset.first()
            comp_serializer = CompetitionMScoresSerializer_H2h(comp, context={'request':request})
            return Response(comp_serializer.data, status=status.HTTP_200_OK)
        
        bracket_comp_qset = BracketMatchup.objects.filter(uuid=uuid)
        if bracket_comp_qset.exists():
            comp = bracket_comp_qset.first()
            comp_serializer = CompetitionMScoresSerializer_Bracket(comp, context={'request':request})
            return Response(comp_serializer.data, status=status.HTTP_200_OK)
        
        return ResourceWarning(status=status.HTTP_404_NOT_FOUND)
    


class GetCompInd(APIView):
    def get(self, request, uuid):
        comp = get_object_or_404(Competition_Ind, uuid=uuid)
        serializer = CompetitionMScoresSerializer_Ind(comp, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetCompTeam(APIView):
    def get(self, request, uuid):
        comp = get_object_or_404(Competition_Team, uuid=uuid)
        serializer = CompetitionMScoresSerializer_Team(comp, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)