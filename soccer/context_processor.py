from django.db.models import Q
from soccer.models import PlayerDetails, Stat

def total_soccer_counts(request):
    # Filter PlayerDetails based on related Stat's odds for 'bet365' and 'kambi'
    soccer_total = PlayerDetails.objects.filter(
        stat__odds__sportsbook_name__in=['bet365', 'kambi']  # Filter based on odds from 'bet365' and 'kambi'
    ).distinct().count()  # Ensures no duplicates and counts the result

    return {
        "soccer_total": soccer_total,
    }
