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


User = get_user_model()

def convert_to_img_file(base_64_img):
    format, imgstr = base_64_img.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data

# Create your views here.
class CreateAllLeagueView(APIView):
    def post(self, request):
        league_data = request.data.get('league')
        league_img_b64 = league_data.get('img')
        league_data['img'] = convert_to_img_file(league_img_b64)

        brolympics_data = request.data.get('brolympics')
        brolympics_img_b64 = brolympics_data.get('img')
        brolympics_data['img'] = convert_to_img_file(brolympics_img_b64)

        h2h_event_data = request.data.get('h2h_event')
        ind_event_data = request.data.get('ind_event')
        team_event_data = request.data.get('team_event')

        league_serializer = LeagueCreateSerializer(data=league_data, context={'request': request})
        brolympics_serializer = BrolympicsCreateSerializer(data=brolympics_data)

        if league_serializer.is_valid():
            league = league_serializer.save()
        else:
            return Response(league_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        brolympics_data['league'] = league.id
        if brolympics_serializer.is_valid():
            brolympics = brolympics_serializer.save()
        else:
            return Response(brolympics_serializer.errors, status=400)

        for event_data_list in [h2h_event_data, ind_event_data, team_event_data]:
            for event_data in event_data_list:
                event_data['brolympics'] = brolympics.id


        h2h_serializer = EventH2HCreateAllSerializer(data=h2h_event_data, many=True)
        ind_serializer = EventIndCreateAllSerializer(data=ind_event_data, many=True) 
        team_serializer = EventTeamCreateAllSerializer(data=team_event_data, many=True) 

        if h2h_serializer.is_valid():
            h2h_serializer.save()
        else:
            return Response(h2h_serializer.errors, status=400)

        if ind_serializer.is_valid():
            ind_serializer.save()
        else:
            return Response(ind_serializer.errors, status=400)

        if team_serializer.is_valid():
            team_serializer.save()
        else:
            return Response(team_serializer.errors, status=400)
        

        all_league_serializer = AllLeaguesSerializer(league, context={'request' : request})
        return Response(all_league_serializer.data, status=status.HTTP_201_CREATED )

class CreateLeagueView(APIView):
    def post(self, request):
        pass


class GetAllLeagues(APIView):
    serializer_class = AllLeaguesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        leagues_as_owner = user.league_set.all()
        leagues_as_player = user.leagues.all()

        leagues = (leagues_as_player | leagues_as_owner).distinct() 
        serializer = self.serializer_class(leagues, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetLeagueInfo(APIView):
    serializer_class = AllLeaguesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        league = get_object_or_404(League, uuid=uuid)
        serializer = self.serializer_class(league, context={'request' : request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JoinLeague(APIView):
    def post(self, request, uuid):
        league = get_object_or_404(League, uuid=uuid)
        user = request.user
        league.players.add(user)

        return Response(status=status.HTTP_200_OK)
        
class GetBrolympicsInfo(APIView):
    serializer_class = AllLeaguesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        broylmpics = get_object_or_404(Brolympics, uuid=uuid)
        serializer = self.serializer_class(broylmpics)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JoinBrolympics(APIView):
    def post(self, request, uuid):
        brolympics = get_object_or_404(Brolympics, uuid=uuid)
        league = brolympics.league
        user = request.user

        brolympics.players.add(user)
        league.players.add(user)

        return Response(status=status.HTTP_200_OK)
        

class GetTeamInfo(APIView):
    serializer_class = AllLeaguesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        team = get_object_or_404(Team, uuid=uuid)
        serializer = self.serializer_class(team)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JoinTeam(APIView):
    def post(self, request, uuid):
        team = get_object_or_404(Team, uuid=uuid)
        user = request.user
        team.add_player(user)

        return Response(status=status.HTTP_200_OK)
        