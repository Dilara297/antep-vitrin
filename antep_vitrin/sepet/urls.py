from django.urls import path
from . import views

urlpatterns = [
    path('ekle/<int:urun_id>/', views.sepete_ekle, name='sepete_ekle'),
    path('detay/', views.sepet_detay, name='sepet_detay'),
    path('cikar/<int:urun_id>/', views.sepetten_cikar, name='sepetten_cikar'),
    path('tamamla/', views.siparisi_tamamla, name='siparisi_tamamla'),
    path('siparislerim/', views.siparislerim, name='siparislerim'),
]