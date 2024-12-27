from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_soccer_data, name='soccer')
]