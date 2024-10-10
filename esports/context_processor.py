from .models import EsportData

def total_esport_counts(request):
    return {
        "csgo_total": EsportData.objects.filter(sport="CSGO").count(),
        "val_total": EsportData.objects.filter(sport="VAL").count(),
        "cod_total": EsportData.objects.filter(sport="COD").count(),
        "lol_total": EsportData.objects.filter(sport="LOL").count(),
        "dota2_total": EsportData.objects.filter(sport="DOTA").count(),
        "halo_total": EsportData.objects.filter(sport="HALO").count()
    }
