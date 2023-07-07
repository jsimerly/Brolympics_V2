from django.urls import path
from brolympics.views import CreateLeagueView

urlpatterns = [
    path('create-league/', CreateLeagueView.as_view(), name='create_league'),

]
