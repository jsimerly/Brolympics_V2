from django.urls import path
from brolympics.views import *
from brolympics.active_views import *

urlpatterns = [
    #Create
    path('create-all-league/', CreateAllLeagueView.as_view(), name='create_all_league'),
    path('create-single-team/', CreateSingleTeam.as_view(), name='create_single_team'),

    #Get
    path('all-leagues/', GetAllLeagues.as_view(), name='get_all_leagues'),
    path('league-info/<uuid:uuid>', GetLeagueInfo.as_view(), name='get_league_info'),
    path('get-brolympics-home/<uuid:uuid>', GetBrolympicsHome.as_view(), name='get_brolympics_home'),
    path('upcoming/', GetUpcoming.as_view(), name='get_upcoming'),
    path('league-teams/<uuid:uuid>', GetLeagueTeams.as_view(), name='league_teams'),
    
    #Update
    path('update-event/', UpdateEvent.as_view(), name='update_event'),

    #Delete
    path('delete-team/<uuid:uuid>', DeleteTeam.as_view(), name='delete_team'),
    path('remove-player-team/<uuid:player_uuid>/<uuid:team_uuid>', RemovePlayerFromTeam.as_view(), name='remove_player_from_team'),

    #invites
    path('league-invite/<uuid:uuid>', GetLeagueInvite.as_view(), name='league_invite'),
    path('join-league/<uuid:uuid>', JoinLeague.as_view(), name='join_league'),
    path('brolympics-invite/<uuid:uuid>', GetBrolympicsInvite.as_view(), name='brolympics_invite'),
    path('join-brolympics/<uuid:uuid>', JoinBrolympics.as_view(), name='join_brolympics'),
    path('team-invite/<uuid:uuid>', GetTeamInvite.as_view(), name='team_invite'),
    path('join-team/<uuid:uuid>', JoinTeam.as_view(), name='join_team'),

    #Active Brolympics
    path('start-brolympics/', StartBrolympics.as_view(), name='start_brolympics'),
    path('events-unstarted/<uuid:uuid>', UnstartedEvents.as_view(), name='unstarted-events'),
    path('start-event/', StartEvents.as_view(), name='start_event'),
]
