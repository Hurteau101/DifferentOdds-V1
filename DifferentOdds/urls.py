from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from admin_panel import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('esports/', include('esports.urls')),
    path('', include('users.urls')),
    path('', lambda request: redirect('login')),
    path('admin-panel', views.admin_panel, name='admin_panel'),
]