from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from vitrin.models import Urun
from .models import Sepet, SepetUrunu
from django.db import transaction

def sepete_ekle(request, urun_id):
    # 1. Hangi yöresel ürün eklenecek buluyoruz
    urun = get_object_or_404(Urun, id=urun_id)
    
    # 2. Sepeti bul veya oluştur (Kullanıcı giriş yaptıysa user, yapmadıysa session_id ile)
    if request.user.is_authenticated:
        sepet, created = Sepet.objects.get_or_create(user=request.user)
    else:
        # Tarayıcıda henüz bir session (oturum) yoksa, hemen bir tane başlatıyoruz
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        # user=None şartını koyuyoruz ki başkasının sepetiyle karışmasın
        sepet, created = Sepet.objects.get_or_create(session_id=session_id, user=None)
        
    # 3. Ürünü sepete ekle. Zaten varsa sadece adedini 1 artır.
    sepet_urunu, created = SepetUrunu.objects.get_or_create(sepet=sepet, urun=urun)
    if not created:
        sepet_urunu.adet += 1
        sepet_urunu.save()
        
    return JsonResponse({
        'mesaj': f'{urun.isim} sepete eklendi.',
        'sepetteki_adet': sepet_urunu.adet
    })
    
def sepet_detay(request):
    # 1. Önce kullanıcının sepetini buluyoruz (Üye mi yoksa misafir mi kontrolüyle)
    if request.user.is_authenticated:
        sepet = Sepet.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        sepet = Sepet.objects.filter(session_id=session_id, user=None).first()
        
    # 2. Sepet hiç oluşmamışsa veya içi boşsa
    if not sepet or not sepet.urunler.exists():
        return JsonResponse({
            'mesaj': 'Sepetiniz şu an boş.', 
            'urunler': [], 
            'genel_toplam': 0
        })
        
    # 3. Sepet doluysa içindeki ürünleri döngüye sokup hesap kitap yapıyoruz
    urunler_listesi = []
    genel_toplam = 0
    
    for kalem in sepet.urunler.all():
        kalem_toplam = kalem.toplam_fiyat_getir() # models.py'de yazdığımız fonksiyon çalışıyor
        genel_toplam += kalem_toplam
        
        urunler_listesi.append({
            'urun_ismi': kalem.urun.isim,
            'adet': kalem.adet,
            'birim_fiyat': kalem.urun.fiyat,
            'kalem_toplam': kalem_toplam
        })
        
    return JsonResponse({
        'mesaj': 'Sepet detayları başarıyla getirildi.',
        'urunler': urunler_listesi,
        'genel_toplam': genel_toplam
    })
    
def sepetten_cikar(request, urun_id):
    # 1. Sepeti bul (Giriş yapan veya misafir)
    if request.user.is_authenticated:
        sepet = Sepet.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        sepet = Sepet.objects.filter(session_id=session_id, user=None).first()
        
    if not sepet:
        return JsonResponse({'hata': 'Sepet bulunamadı.'}, status=404)
        
    # 2. Sepetten çıkarılmak istenen ürünü bul
    sepet_urunu = SepetUrunu.objects.filter(sepet=sepet, urun_id=urun_id).first()
    
    if not sepet_urunu:
        return JsonResponse({'hata': 'Bu ürün sepetinizde yok.'}, status=404)
        
    # 3. Kritik Karar: Adet 1'den büyükse sadece eksilt, 1 ise satırı tamamen sil
    if sepet_urunu.adet > 1:
        sepet_urunu.adet -= 1
        sepet_urunu.save()
        mesaj = f'{sepet_urunu.urun.isim} adedi 1 azaltıldı. Kalan adet: {sepet_urunu.adet}'
    else:
        sepet_urunu.delete()
        mesaj = f'{sepet_urunu.urun.isim} sepetten tamamen çıkarıldı.'
        
    return JsonResponse({'mesaj': mesaj})

def siparisi_tamamla(request):
    # 1. Sepeti bul
    if request.user.is_authenticated:
        sepet = Sepet.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        sepet = Sepet.objects.filter(session_id=session_id, user=None).first()
        
    if not sepet or not sepet.urunler.exists():
        return JsonResponse({'hata': 'Sepetiniz boş, sipariş verilemez.'}, status=400)
        
    try:
        # transaction.atomic() ile işlemleri mühürlüyoruz. 
        # Hata çıkarsa her şey geri alınır (Rollback).
        with transaction.atomic():
            genel_toplam = 0
            
            for kalem in sepet.urunler.all():
                genel_toplam += kalem.toplam_fiyat_getir()
                
            # Sipariş başarıyla alındığı için kullanıcının sepetindeki kalemleri siliyoruz
            sepet.urunler.all().delete()
            
        return JsonResponse({
            'mesaj': 'Siparişiniz başarıyla alındı. Afiyet olsun!',
            'odenen_tutar': genel_toplam
        })
        
    except Exception as e:
        return JsonResponse({'hata': f'Sipariş sırasında kritik bir hata oluştu: {str(e)}'}, status=500)