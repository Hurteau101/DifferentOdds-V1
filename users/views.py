from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import UserAlert
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def create_user(request):
    if request.user.is_authenticated:
        return redirect('csgo')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('csgo')

    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get() to avoid KeyError
        password = request.POST.get('password')  # Use .get() to avoid KeyError


        user_exist = User.objects.filter(username=username.lower()).exists()

        if user_exist:
            user = authenticate(request, username=username.lower(), password=password)

            if user is not None:
                login(request, user)
                return redirect('csgo')
            else:
                messages.error(request, 'Username or password is incorrect')
        else:
            messages.error(request, 'Username not found')

    return render(request, 'login.html')

def forgot_password(request):
    return render(request, 'reset_password.html')


@login_required
def get_user_alerts(request):
    alerts = UserAlert.objects.filter(user=request.user, acknowledged=False)
    alerts_data = [{'id': alert.id, 'message': alert.message} for alert in alerts]
    return JsonResponse({'alerts': alerts_data})


@require_POST
@login_required
def acknowledge_alert(request):
    try:
        data = json.loads(request.body)
        alert_id = data.get('alert_id')
        if alert_id:
            alert = UserAlert.objects.get(id=alert_id, user=request.user)
            alert.acknowledged = True
            alert.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid alert ID'}, status=400)
    except (json.JSONDecodeError, UserAlert.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)