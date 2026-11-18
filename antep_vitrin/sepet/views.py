import json
import random
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from vitrin.models import Urun
from .models import Sepet, SepetUrunu, Siparis, SiparisUrunu
from hesap.models import Profil

def sepete_ekle(request, urun_id):
    if not request.user.is_authenticated:
        return JsonResponse({'hata': 'Sepete ürün eklemek için önce giriş yapmalısınız.'}, status=401)

    urun = get_object_or_404(Urun, id=urun_id)
    sepet, _ = Sepet.objects.get_or_create(user=request.user)
    
    sepet_urunu, created = SepetUrunu.objects.get_or_create(sepet=sepet, urun=urun)
    if not created:
        sepet_urunu.adet += 1
        sepet_urunu.save()
        
    return JsonResponse({
        'mesaj': f'{urun.isim} sepete eklendi.',
        'sepetteki_adet': sepet_urunu.adet
    })

@login_required(login_url='giris_yap')
def sepet_detay(request):
    sepet = Sepet.objects.filter(user=request.user).first()
    profil_obj = Profil.objects.filter(user=request.user).first()
    kayitli_adres = profil_obj.adres if profil_obj and profil_obj.adres else ''
        
    if not sepet or not sepet.urunler.exists():
        return render(request, 'sepet/sepet_detay.html', {
            'urunler': [],
            'genel_toplam': 0,
            'kayitli_adres': kayitli_adres
        })
        
    urunler_listesi = []
    genel_toplam = 0
    
    for kalem in sepet.urunler.all():
        kalem_toplam = kalem.toplam_fiyat_getir()
        genel_toplam += kalem_toplam
        
        urunler_listesi.append({
            'id': kalem.urun.id,
            'urun_ismi': kalem.urun.isim,
            'adet': kalem.adet,
            'birim_fiyat': kalem.urun.fiyat,
            'kalem_toplam': kalem_toplam,
            'gorsel_url': kalem.urun.gorsel.url if kalem.urun.gorsel else None
        })
        
    return render(request, 'sepet/sepet_detay.html', {
        'urunler': urunler_listesi,
        'genel_toplam': genel_toplam,
        'kayitli_adres': kayitli_adres
    })

def sepetten_cikar(request, urun_id):
    if not request.user.is_authenticated:
        return JsonResponse({'hata': 'Bu işlem için giriş yapmalısınız.'}, status=401)

    sepet = Sepet.objects.filter(user=request.user).first()
    if not sepet:
        return JsonResponse({'hata': 'Sepet bulunamadı.'}, status=404)
        
    sepet_urunu = SepetUrunu.objects.filter(sepet=sepet, urun_id=urun_id).first()
    if not sepet_urunu:
        return JsonResponse({'hata': 'Bu ürün sepetinizde yok.'}, status=404)
        
    if sepet_urunu.adet > 1:
        sepet_urunu.adet -= 1
        sepet_urunu.save()
        mesaj = f'{sepet_urunu.urun.isim} adedi 1 azaltıldı. Kalan adet: {sepet_urunu.adet}'
    else:
        sepet_urunu.delete()
        mesaj = f'{sepet_urunu.urun.isim} sepetten tamamen çıkarıldı.'
        
    return JsonResponse({'mesaj': mesaj})

def siparisi_tamamla(request):
    if not request.user.is_authenticated:
        return JsonResponse({'hata': 'Sipariş vermek için giriş yapmalısınız.'}, status=401)

    sepet = Sepet.objects.filter(user=request.user).first()
    if not sepet or not sepet.urunler.exists():
        return JsonResponse({'hata': 'Sepetiniz boş, sipariş verilemez.'}, status=400)

    teslimat_adresi = ""
    if request.method == 'POST':
        try:
            veri = json.loads(request.body)
            teslimat_adresi = veri.get('teslimat_adresi', '')
        except json.JSONDecodeError:
            pass

    try:
        with transaction.atomic():
            takip_no = f"TR{random.randint(10000000, 99999999)}"
            siparis = Siparis.objects.create(
                user=request.user,
                teslimat_adresi=teslimat_adresi,
                kargo_takip_no=takip_no
            )

            genel_toplam = 0
            for kalem in sepet.urunler.all():
                kalem_toplam = kalem.toplam_fiyat_getir()
                genel_toplam += kalem_toplam
                
                SiparisUrunu.objects.create(
                    siparis=siparis,
                    urun=kalem.urun,
                    adet=kalem.adet,
                    birim_fiyat=kalem.urun.fiyat
                )
                
            siparis.odenen_tutar = genel_toplam
            siparis.save()
            sepet.urunler.all().delete()
            
        return JsonResponse({
            'mesaj': f'Sipariş #{siparis.id} başarıyla alındı.',
            'odenen_tutar': genel_toplam,
            'takip_no': takip_no
        })
    except Exception as e:
        return JsonResponse({'hata': f'Sipariş sırasında kritik bir hata oluştu: {str(e)}'}, status=500)

@login_required(login_url='giris_yap')
def siparislerim(request):
    siparisler = Siparis.objects.filter(user=request.user).order_by('-olusturulma_tarihi')
    return render(request, 'sepet/siparislerim.html', {'siparisler': siparisler})