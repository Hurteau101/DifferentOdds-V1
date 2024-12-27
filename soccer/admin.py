from django.contrib import admin
from soccer.models import PlayerDetails, Stat, SportsbookOdds

# Register your models here.
admin.site.register(PlayerDetails)
admin.site.register(Stat)
admin.site.register(SportsbookOdds)