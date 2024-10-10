import requests
from django.db import transaction
from .models import EsportData
from DifferentOdds.celery import app

def get_api_data():
    return requests.get("https://esportsdifference.com/compare").json()

@app.task
@transaction.atomic
def get_data():
    data = get_api_data()
    EsportData.objects.all().delete()

    add_player_objects_to_create = []
    player_batch_size = 100

    for key, value in data.items():
        if value is not None:
            for esport in value:
                add_player_objects_to_create.append(EsportData(
                    player_name=esport['player'],
                    team_name=esport['team'],
                    opponent_name=esport['opponent'],
                    sport=esport['sport'],
                    stat_type=esport['stat_type'],
                    prizepick=esport['prize_picks'],
                    underdog=esport['underdog'],
                    projection_string=esport['projection_string'],
                    difference=esport['difference'],
                    difference_percentage=esport['percent_difference'],
                    timestamp=esport['timestamp']
                ))

    EsportData.objects.bulk_create(add_player_objects_to_create, player_batch_size)

