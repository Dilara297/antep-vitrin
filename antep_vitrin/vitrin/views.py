from django.shortcuts import render,get_object_or_404
from .models import Urun, Kategori

def ana_sayfa(request):
    kategoriler = Kategori.objects.all()
    secili_kategori_id = request.GET.get('kategori')

    if secili_kategori_id and secili_kategori_id.isdigit():
        urunler = Urun.objects.filter(kategori_id=int(secili_kategori_id))
        secili_kategori_id = int(secili_kategori_id)
    else:
        urunler = Urun.objects.all()
        secili_kategori_id = None

    return render(request, 'vitrin/ana_sayfa.html', {
        'kategoriler': kategoriler,
        'urunler': urunler,
        'secili_kategori_id': secili_kategori_id,
    })
def urun_detay(request, slug):
    urun = get_object_or_404(Urun, slug=slug, stokta_var=True)
    return render(request, 'vitrin/urun_detay.html', {'urun': urun})