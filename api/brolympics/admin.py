from django.contrib import admin
from brolympics.models import *

# Register your models here.
admin.site.register(League)
admin.site.register(Brolympics)
admin.site.register(Event)
admin.site.register(OverallBrolympicsRanking)
admin.site.register(Team)
admin.site.register(IndividualCompetition)
admin.site.register(H2hCompetition)
admin.site.register(EventRanking_Individual)
admin.site.register(EventRanking_H2H)