from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_test_view, name='soccer')
]