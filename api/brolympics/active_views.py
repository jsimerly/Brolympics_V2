from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from brolympics.models import *
from brolympics.serializers import *
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
    
