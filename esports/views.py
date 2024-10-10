from django.shortcuts import render, redirect
from esports.tasks import get_api_data, get_data
from esports.models import EsportData
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def load_cod(request):
    stat_types = set(EsportData.objects.filter(sport="COD").values_list('stat_type', flat=True))
    teams = set(EsportData.objects.filter(sport="COD").values_list('team_name', flat=True))

    esport_data = EsportData.objects.filter(sport='COD')


    context = {
        'esport_data': esport_data,
        'esport_name': "Call of Duty",
        'stat_types': stat_types,
        "teams": teams
    }

    return render(request, 'esports_table.html', context)

@login_required(login_url='login')
def load_csgo(request):
    stat_types = set(EsportData.objects.filter(sport="CSGO").values_list('stat_type', flat=True))
    teams = set(EsportData.objects.filter(sport="CSGO").values_list('team_name', flat=True))

    esport_data = EsportData.objects.filter(sport='CSGO')

    context = {
        'esport_data': esport_data,
        'esport_name': "Counter-Strike 2",
        'stat_types': stat_types,
        "teams": teams,
    }

    return render(request, 'esports_table.html', context)

@login_required(login_url='login')
def load_lol(request):
    stat_types = set(EsportData.objects.filter(sport="LOL").values_list('stat_type', flat=True))
    teams = set(EsportData.objects.filter(sport="LOL").values_list('team_name', flat=True))

    esport_data = EsportData.objects.filter(sport='LOL')

    context = {
        'esport_data': esport_data,
        'esport_name': "League of Legends",
        'stat_types': stat_types,
        "teams": teams
    }

    return render(request, 'esports_table.html', context)

@login_required(login_url='login')
def load_val(request):
    stat_types = set(EsportData.objects.filter(sport="VAL").values_list('stat_type', flat=True))
    teams = set(EsportData.objects.filter(sport="VAL").values_list('team_name', flat=True))

    esport_data = EsportData.objects.filter(sport='VAL')

    context = {
        'esport_data': esport_data,
        'esport_name': "Valorant",
        'stat_types': stat_types,
        "teams": teams
    }

    return render(request, 'esports_table.html', context)

@login_required(login_url='login')
def load_dota2(request):
    stat_types = set(EsportData.objects.filter(sport="DOTA").values_list('stat_type', flat=True))
    teams = set(EsportData.objects.filter(sport="DOTA").values_list('team_name', flat=True))

    esport_data = EsportData.objects.filter(sport='DOTA')

    context = {
        'esport_data': esport_data,
        'esport_name': "DOTA 2",
        'stat_types': stat_types,
        "teams": teams
    }

    return render(request, 'esports_table.html', context)

@login_required(login_url='login')
def load_halo(request):
    stat_types = set(EsportData.objects.filter(sport="HALO").values_list('stat_type', flat=True))
    teams = set(EsportData.objects.filter(sport="HALO").values_list('team_name', flat=True))

    esport_data = EsportData.objects.filter(sport='HALO')

    context = {
        'esport_data': esport_data,
        'esport_name': "HALO",
        'stat_types': stat_types,
        "teams": teams
    }
    return render(request, 'esports_table.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')
