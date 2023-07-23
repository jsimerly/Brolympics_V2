from django.urls import path
from brolympics.views import *

urlpatterns = [
    path('create-league/', CreateLeagueView.as_view(), name='create_league'),
    path('create-all-league/', CreateAllLeagueView.as_view(), name='create_all_league'),
    path('all-leagues/', GetAllLeagues.as_view(), name='get_all_leagues'),
]
