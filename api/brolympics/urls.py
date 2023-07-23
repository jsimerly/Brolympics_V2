from django.urls import path
from brolympics.views import *

urlpatterns = [
    path('create-league/', CreateLeagueView.as_view(), name='create_league'),
    path('create-all-league/', CreateAllLeagueView.as_view(), name='create_all_league'),
    path('all-leagues/', GetAllLeagues.as_view(), name='get_all_leagues'),

    #invites
    path('league-invite/<uuid:uuid>', GetLeagueInfo.as_view(), name='league_invite'),
    path('join-league/<uuid:uuid>', JoinLeague.as_view(), name='join_league'),
    path('brolympics-invite/<uuid:uuid>', GetBrolympicsInfo.as_view(), name='brolympics_invite'),
    path('join-brolympics/<uuid:uuid>', JoinBrolympics.as_view(), name='join_brolympics'),
    path('team-invite/<uuid:uuid>', GetTeamInfo.as_view(), name='team_invite'),
    path('join-team/<uuid:uuid>', JoinTeam.as_view(), name='join_team'),
]
