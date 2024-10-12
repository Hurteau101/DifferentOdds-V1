from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('esports/', include('esports.urls')),
    path('', include('users.urls')),
    path('', lambda request: redirect('login'))
]
