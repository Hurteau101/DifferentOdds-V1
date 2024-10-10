from django.urls import path
from . import views

urlpatterns = [
    path('cod', views.load_cod, name='cod'),
    path('csgo', views.load_csgo, name='csgo'),
    path('lol', views.load_lol, name='lol'),
    path('val', views.load_val, name='val'),
    path('dota2', views.load_dota2, name='dota2'),
    path('halo', views.load_halo, name='halo'),
    path('logout', views.logout_user, name='logout'),
]