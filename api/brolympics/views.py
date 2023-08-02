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


User = get_user_model()

def convert_to_img_file(base_64_img):
    if base_64_img is None:
        return None
    
    format, imgstr = base_64_img.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data

# Create your views here.


class CreateAllLeagueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        league_data = request.data.get('league')
        league_img_b64 = league_data.get('img')
        league_data['img'] = convert_to_img_file(league_img_b64)

        brolympics_data = request.data.get('brolympics')
        brolympics_img_b64 = brolympics_data.get('img')
        brolympics_data['img'] = convert_to_img_file(brolympics_img_b64)

        h2h_event_data = request.data.get('h2h_events')
        ind_event_data = request.data.get('ind_events')
        team_event_data = request.data.get('team_events')

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
            print(h2h_serializer.errors)
            return Response(h2h_serializer.errors, status=400)

        if ind_serializer.is_valid():
            ind_serializer.save()
        else:
            print(ind_serializer.errors)
            return Response(ind_serializer.errors, status=400)

        if team_serializer.is_valid():
            team_serializer.save()
        else:
            print(team_serializer.errors)
            return Response(team_serializer.errors, status=400)
        

        all_league_serializer = AllLeaguesSerializer(league, context={'request' : request})
        return Response(all_league_serializer.data, status=status.HTTP_201_CREATED )
    
class CreateSingleTeam(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            join_team = request.data.get('user_join')
            team = serializer.save()
            print(join_team)
            if join_team:
                print('adding?')
                team.add_player(request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateSingleEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('event_name')
        type = request.data.get('type')
        bro_uuid = request.data.get('uuid')
        brolympics = Brolympics.objects.get(uuid=bro_uuid)

        if type == 'h2h':
            Event_H2H.objects.create(brolympics=brolympics, name=name)

        if type == 'ind':
            Event_IND.objects.create(brolympics=brolympics, name=name)

        if type == 'team':
            Event_Team.objects.create(brolympics=brolympics, name=name)

        return Response(status=status.HTTP_200_OK)


# Get Info
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
    serializer_class = LeagueInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        league = get_object_or_404(League, uuid=uuid)
        serializer = self.serializer_class(league, context={'request' : request})


        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
class GetBrolympicsHome(APIView):
    serializer_class = BrolympicsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        brolympics = get_object_or_404(Brolympics, uuid=uuid)
        serializer = self.serializer_class(brolympics, context={'request':request})

        ## Need a new serializer to get active events
        #this will need to be a check, then we feed it to a different serializer to get the information we need. [pre, active, post]
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetUpcoming(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user


        brolympics = Brolympics.objects.filter(players__in=[user])
        upcoming_bro = brolympics.filter(start_time__isnull=True, is_complete=False)
        current_bro = Brolympics.objects.filter(start_time__isnull=False, is_complete=False)

        upcoming_comp_h2h = Competition_H2H.objects.filter(
            Q(team_1__player_1=user) | Q(team_1__player_2=user) | 
            Q(team_2__player_1=user) | Q(team_2__player_2=user),
            is_complete=False,
            start_time=None
        )
        upcoming_bracket_matchup = BracketMatchup.objects.filter(
            Q(team_1__player_1=user) | Q(team_1__player_2=user) | 
            Q(team_2__player_1=user) | Q(team_2__player_2=user),
            is_complete=False,
            start_time=None
        )
        upcoming_comp_ind = Competition_Ind.objects.filter(
            Q(team__player_1=user) | Q(team__player_2=user),
            is_complete=False,
            start_time=None
        )
        upcoming_comp_team = Competition_Team.objects.filter(
            Q(team__player_1=user) | Q(team__player_2=user),
            is_complete=False,
            start_time=None
        )

        upcoming_bro_serializer = BrolympicsSerializer(upcoming_bro, context={'request':request}, many=True)
        current_bro_serializer = BrolympicsSerializer(current_bro, context={'request':request}, many=True)

        h2h_serializer = CompetitionSerializer_H2h(upcoming_comp_h2h, many=True)
        bracket_serializer = BracketCompetitionSerializer_H2h(upcoming_bracket_matchup, many=True)
        ind_serializer = CompetitionSerializer_Ind(upcoming_comp_ind, many=True)
        team_serializer = CompetitionSerializer_Team(upcoming_comp_team, many=True)


        data = {
            'current_brolympics' :  current_bro_serializer.data,
            'upcoming_brolympics' : upcoming_bro_serializer.data,
            'upcoming_competitions' : h2h_serializer.data + bracket_serializer.data + ind_serializer.data + team_serializer.data
        }
        

        return Response(data, status=status.HTTP_200_OK)
    
class GetLeagueTeams(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        pass


## Updates ##
class UpdateEvent(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        event_uuid = request.data.get('uuid')
        event_type = request.data.get('type')

        if event_type == 'h2h':
            event = get_object_or_404(Event_H2H, uuid=event_uuid)
            serializer = EventBasicSerializer_H2h(event, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        elif event_type == 'ind':
            event = get_object_or_404(Event_IND, uuid=event_uuid)
            serializer = EventBasicSerializer_Ind(event, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        elif event_type == 'team':
            event = get_object_or_404(Event_Team, uuid=event_uuid)
            serializer = EventBasicSerializer_Team(event, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

## Delete ##

class DeleteTeam(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid):
        team = get_object_or_404(Team, uuid=uuid)

        if self.request.user != team.player_1 and \
            self.request.user != team.player_2 and \
            self.request.user != team.brolympics.league.league_owner:
            raise PermissionDenied("You do not have permission to delete this league.")
        return team

    def delete(self, request, uuid):
        team = self.get_object(uuid)
        team.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RemovePlayerFromTeam(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, player_uuid, team_uuid):
        player = get_object_or_404(User, uuid=player_uuid)
        team = get_object_or_404(Team, uuid=team_uuid)

        if self.request.user != team.player_1 and self.request.user != team.player_2 and self.request.user !=  team.brolympics.league.league_owner:
            raise PermissionDenied("You do not have permission to remove this player from this team.")
        return player, team     

    def delete(self, request, player_uuid, team_uuid):
        player, team = self.get_object(player_uuid, team_uuid)
        team.remove_player(player)

        return Response(status=status.HTTP_204_NO_CONTENT)

## Invites ##
class GetLeagueInvite(APIView):
    serializer_class = AllLeaguesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid):
        league = get_object_or_404(League, uuid=uuid)
        
        return league

    def get(self, request, uuid):
        league = self.get_object(uuid)
        serializer = self.serializer_class(league, context={'request' : request})

        return Response(serializer.data, status=status.HTTP_200_OK)
        

    
class JoinLeague(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        league = get_object_or_404(League, uuid=uuid)
        user = request.user
        league.players.add(user)

        data = {
            'league_uuid':league.uuid, 
            'welcome_message' : f'Your request to join was successful. Welcome to {league.name}'
        }

        return Response(data,status=status.HTTP_200_OK)
        
class GetBrolympicsInvite(APIView):
    serializer_class = BrolympicsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        broylmpics = get_object_or_404(Brolympics, uuid=uuid)
        serializer = self.serializer_class(broylmpics)

        return Response(serializer.data, status=status.HTTP_200_OK)
            
class JoinBrolympics(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, uuid):
        brolympics = get_object_or_404(Brolympics, uuid=uuid)
        league = brolympics.league
        user = request.user

        brolympics.players.add(user)
        league.players.add(user)

        data = {
            'bro_uuid':brolympics.uuid, 
            'welcome_message' : f'Your request to join was successful. Welcome to {brolympics.name}'
        }

        return Response(data, status=status.HTTP_200_OK)
        

class GetTeamInvite(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        team = get_object_or_404(Team, uuid=uuid)
        serializer = self.serializer_class(team, context={'request':request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)   
             
class JoinTeam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        team = get_object_or_404(Team, uuid=uuid)
        user = request.user
        team.brolympics.players.add(user)
        team.brolympics.league.players.add(user)
        try:
            team.add_player(user)
        except ValueError as e:
            Response({'detail':str(e)},status=status.HTTP_409_CONFLICT)

        data = {
            'bro_uuid':team.brolympics.uuid, 
            'welcome_message' : f'Your request to join was successful. Welcome to {team.name}'
        }

        return Response(data,status=status.HTTP_200_OK)
        