from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import UserProfile


def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('csgo')

    return _wrapped_view_func


# Create your views here.
@admin_required
def admin_panel(request):
    users = User.objects.all()

    user_data = []
    for user in users:
        # Get the associated UserProfile object for each user
        profile = UserProfile.objects.filter(user=user).first()
        user_data.append({
            'username': user.username,
            'email': user.email,
            'discord_username': profile.discord_username if profile else 'N/A',
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'N/A',
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        })

    return render(request, 'admin_panel.html', {'user_data': user_data})
