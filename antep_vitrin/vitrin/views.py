from django.shortcuts import render,get_object_or_404
from .models import Urun, Kategori

def ana_sayfa(request):
    urunler = Urun.objects.filter(stokta_var=True).order_by('-eklenme_tarihi')
    kategoriler = Kategori.objects.all()
    return render(request, 'vitrin/ana_sayfa.html', {'urunler': urunler, 'kategoriler': kategoriler})

def urun_detay(request, slug):
    urun = get_object_or_404(Urun, slug=slug, stokta_var=True)
    return render(request, 'vitrin/urun_detay.html', {'urun': urun})