from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

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