import uuid

from django.db import models


class PlayerDetails(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    player_name = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    opponent = models.CharField(max_length=200)
    game_date_time = models.DateTimeField()

    class Meta:
        unique_together = ('player_name', 'game_date_time')

    def __str__(self):
        return f"{self.player_name}"

# PUT TEAM AS A RELATIONSHIP
class Stat(models.Model):
    player = models.ForeignKey(PlayerDetails, on_delete=models.CASCADE)
    stat_type = models.CharField(max_length=100)
    line_value = models.FloatField()
    over_multiplier = models.FloatField(null=True, blank=True)
    under_multiplier = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.player_name} {self.stat_type} - {self.line_value}"

class SportsbookOdds(models.Model):
    sportsbook_name = models.CharField(max_length=100)  # e.g., 'bet365' or 'kambi'
    stat = models.ForeignKey(Stat, related_name='odds', on_delete=models.CASCADE)
    american_odds = models.CharField(max_length=100)
    over_under = models.CharField(max_length=10, null=True, blank=True)  # e.g., 'Over' or 'Under'

    def __str__(self):
        return f"{self.sportsbook_name} Odds - {self.american_odds} ({self.over_under}) - {self.stat.player.player_name}"