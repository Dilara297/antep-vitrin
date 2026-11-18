from django.urls import path
from . import views

urlpatterns = [
    path('kayit/', views.kayit_ol, name='kayit_ol'),
    path('giris/', views.giris_yap, name='giris_yap'),
    path('cikis/', views.cikis_yap, name='cikis_yap'),
    path('profil/', views.profil, name='profil'),
]