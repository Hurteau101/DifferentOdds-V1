import json
from pprint import pprint

import requests
from django.db import transaction

from soccer.models import PlayerDetails, Stat, SportsbookOdds


class Soccer:
    def __init__(self):
        pass

    def get_soccer_data(self):
        PlayerDetails.objects.all().delete()

        data = requests.get("https://differentodds-api-d75ec7ff5688.herokuapp.com/dfs_soccer")

        if data.status_code == 200:
            return data.json()
        else:
            print("Error Getting Data")

    def get_soccer_stats(self):
        soccer = self.get_soccer_data()
        if soccer:
            stat_objects = []
            odds_objects = []  # For storing the odds records

            with transaction.atomic():
                for soccer_stats in soccer:
                    # Get or create PlayerDetails without updating existing records
                    player, created = PlayerDetails.objects.get_or_create(
                        player_name=soccer_stats["player_name"],
                        game_date_time=soccer_stats["game_date_time"],
                        defaults={
                            'team': soccer_stats["team"],
                            'opponent': soccer_stats["opponent"],
                        }
                    )

                    # Add stats for bulk insertion
                    for stat in soccer_stats["stats"]:
                        # Create Stat object
                        stat_obj = Stat(
                            player=player,
                            stat_type=stat["stat_type"],
                            line_value=stat["line_value"],
                            over_multiplier=stat["over_multiplier"],
                            under_multiplier=stat["under_multiplier"]
                        )
                        stat_objects.append(stat_obj)

                        # Create SportsbookOdds objects for bet365 and kambi if they exist
                        bet365_odds = stat.get("bet365_odds", [])
                        kambi_odds = stat.get("kambi_odds", [])

                        if bet365_odds:
                            for odds in bet365_odds:
                                odds_objects.append(
                                    SportsbookOdds(
                                        sportsbook_name="bet365",
                                        stat=stat_obj,  # Link to the newly created Stat object
                                        american_odds=odds.get("american_odds"),
                                        over_under=odds.get("over_under")
                                    )
                                )
                        if kambi_odds:
                            for odds in kambi_odds:
                                odds_objects.append(
                                    SportsbookOdds(
                                        sportsbook_name="kambi",
                                        stat=stat_obj,  # Link to the newly created Stat object
                                        american_odds=odds.get("american_odds"),
                                        over_under=odds.get("over_under")
                                    )
                                )

                # Bulk insert Stats and SportsbookOdds
                Stat.objects.bulk_create(stat_objects)
                SportsbookOdds.objects.bulk_create(odds_objects)


