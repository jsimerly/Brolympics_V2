from rest_framework import serializers
from django.contrib.auth import get_user_model
from brolympics.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class HomeEventSerializer_H2h(serializers.ModelSerializer):
    percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = Event_H2H
        fields = ['name', 'uuid', 'percent_complete', 'start_time']

    def get_percent_complete(self, obj):
        return obj.get_percent_complete()
    
class HomeEventSerializer_Ind(serializers.ModelSerializer):
    percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = Event_IND
        fields = ['name', 'uuid', 'percent_complete', 'start_time']

    def get_percent_complete(self, obj):
        return obj.get_percent_complete()
    
class HomeEventSerializer_Team(serializers.ModelSerializer):
    percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = Event_Team
        fields = ['name', 'uuid', 'percent_complete', 'start_time']

    def get_percent_complete(self, obj):
        return obj.get_percent_complete()
