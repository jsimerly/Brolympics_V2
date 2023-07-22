from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from brolympics.models import *
from brolympics.serializers import *

User = get_user_model()


# Create your views here.
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