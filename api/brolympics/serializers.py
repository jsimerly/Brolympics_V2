from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *

User = get_user_model()

class AllLeaguesSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    founded = serializers.SerializerMethodField()

    class Meta:
        model = League
        fields = ['hashid', 'name', 'img' ,'is_owner', 'founded']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.league_owner == request.user
        return False
    
    def get_founded(self, obj):
        return str(obj.founded.year)


