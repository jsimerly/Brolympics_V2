from django.urls import path
from brolympics.views import *

urlpatterns = [
    #create
    path('create-all-league/', CreateAllLeagueView.as_view(), name='create_all_league'),

    #get info
    path('all-leagues/', GetAllLeagues.as_view(), name='get_all_leagues'),
    path('league-info/<uuid:uuid>', GetLeagueInfo.as_view(), name='get_league_info'),
    path('get-brolympics-home/<uuid:uuid>', GetBrolympicsHome.as_view(), name='get_brolympics_home'),
    path('upcoming/', GetUpcoming.as_view(), name='get_upcoming'),
    
    #invites
    path('league-invite/<uuid:uuid>', GetLeagueInvite.as_view(), name='league_invite'),
    path('join-league/<uuid:uuid>', JoinLeague.as_view(), name='join_league'),
    path('brolympics-invite/<uuid:uuid>', GetBrolympicsInvite.as_view(), name='brolympics_invite'),
    path('join-brolympics/<uuid:uuid>', JoinBrolympics.as_view(), name='join_brolympics'),
    path('team-invite/<uuid:uuid>', GetTeamInvite.as_view(), name='team_invite'),
    path('join-team/<uuid:uuid>', JoinTeam.as_view(), name='join_team'),
]
