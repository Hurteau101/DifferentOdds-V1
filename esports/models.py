import uuid
from django.db import models

class EsportData(models.Model):
    player_name = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200)
    opponent_name = models.CharField(max_length=200)
    sport = models.CharField(max_length=10)
    stat_type = models.CharField(max_length=50)
    prizepick = models.FloatField()
    underdog = models.FloatField()
    projection_string = models.CharField(max_length=200)
    difference = models.FloatField()
    difference_percentage = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.player_name} - {self.team_name} vs {self.opponent_name}"