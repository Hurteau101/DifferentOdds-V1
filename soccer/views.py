import json
from pprint import pprint

from django.shortcuts import render
from django.db.models import Q
from soccer.models import PlayerDetails, Stat
from soccer.soccer_extracter import Soccer


def get_soccer_data(requests):
    # Query the Stat model, ensuring only relevant stats with related SportsbookOdds are fetched
    stats_with_odds = Stat.objects.prefetch_related(
        'odds'  # Prefetch related SportsbookOdds for each Stat
    ).filter(
        Q(odds__sportsbook_name='bet365') |
        Q(odds__sportsbook_name='kambi')
    ).distinct()  # Ensures no duplicate stats with odds are fetched

    # Create a custom data structure to store all the relevant data
    data = []
    for stat in stats_with_odds:
        # Fetch Over and Under odds for bet365
        bet365_over = next(
            (odds for odds in stat.odds.all() if odds.sportsbook_name == 'bet365' and odds.over_under == 'Over'), None
        )
        bet365_under = next(
            (odds for odds in stat.odds.all() if odds.sportsbook_name == 'bet365' and odds.over_under == 'Under'), None
        )

        # Fetch Over and Under odds for kambi
        kambi_over = next(
            (odds for odds in stat.odds.all() if odds.sportsbook_name == 'kambi' and odds.over_under == 'Over'), None
        )
        kambi_under = next(
            (odds for odds in stat.odds.all() if odds.sportsbook_name == 'kambi' and odds.over_under == 'Under'), None
        )

        # Append player stats for bet365 Over and Under
        if stat.over_multiplier and (bet365_over or kambi_over):
            data.append({
                'player_name': stat.player.player_name,
                'team': stat.player.team,
                'opponent': stat.player.opponent,
                'game_date_time': stat.player.game_date_time,
                'stat_type': stat.stat_type,
                'line_value': stat.line_value,
                'over_under': 'Over',
                'sportsbook': 'bet365',
                'bet365_odds': bet365_over.american_odds if bet365_over else None,
                'kambi_odds': kambi_over.american_odds if kambi_over else None,
                'multiplier': stat.over_multiplier,
            })
        if stat.under_multiplier and (bet365_under or kambi_under):
            data.append({
                'player_name': stat.player.player_name,
                'team': stat.player.team,
                'opponent': stat.player.opponent,
                'game_date_time': stat.player.game_date_time,
                'stat_type': stat.stat_type,
                'line_value': stat.line_value,
                'over_under': 'Under',
                'sportsbook': 'bet365',
                'bet365_odds': bet365_under.american_odds if bet365_under else None,
                'kambi_odds': kambi_under.american_odds if kambi_under else None,
                'multiplier': stat.under_multiplier,
            })

    team_set =  {data_set["team"] for data_set in data}
    stat_set = {data_set["stat_type"] for data_set in data}
    player_names = {data_set["player_name"] for data_set in data}


    context = {
        "data": data,
        "teams": team_set,
        "stat_types": stat_set,
        "player_names": player_names
    }

    return render(requests, 'soccer_table.html', context)


