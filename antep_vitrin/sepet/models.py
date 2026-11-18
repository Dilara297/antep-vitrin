from django.db import models
from django.contrib.auth.models import User
from vitrin.models import Urun

class Sepet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=250, null=True, blank=True)
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Sepet - {self.user.username}"
        return f"Sepet - Misafir ({self.session_id})"

class SepetUrunu(models.Model):
    sepet = models.ForeignKey(Sepet, on_delete=models.CASCADE, related_name='urunler')
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField(default=1)
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adet} adet {self.urun.isim}"
    
    # Sepetteki o kalemin toplam fiyatını hesaplayan yardımcı fonksiyon
    def toplam_fiyat_getir(self):
        return self.adet * self.urun.fiyat
    
# Kargo durumlarını standart bir listeye (Enum mantığına) bağlıyoruz
KARGO_DURUMLARI = (
    ('Hazırlanıyor', 'Hazırlanıyor'),
    ('Kargoya Verildi', 'Kargoya Verildi'),
    ('Dağıtıma Çıktı', 'Dağıtıma Çıktı'),
    ('Teslim Edildi', 'Teslim Edildi'),
    ('İptal Edildi', 'İptal Edildi'),
)

class Siparis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=250, null=True, blank=True)
    
    # Siparişin kargo ve adres detayları
    teslimat_adresi = models.TextField(blank=True, null=True)
    kargo_durumu = models.CharField(max_length=50, choices=KARGO_DURUMLARI, default='Hazırlanıyor')
    kargo_takip_no = models.CharField(max_length=100, null=True, blank=True)
    kargo_firmasi = models.CharField(max_length=100, default='Aras Kargo')
    
    # Fatura toplamı
    odenen_tutar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Admin panelinde güzel görünmesi için
        if self.user:
            return f"Sipariş #{self.id} - {self.user.username} - {self.kargo_durumu}"
        return f"Sipariş #{self.id} - Misafir - {self.kargo_durumu}"

class SiparisUrunu(models.Model):
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE, related_name='urunler')
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField()
    # Ürünün satın alındığı anki fiyatını dondurup buraya kaydediyoruz
    birim_fiyat = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.adet}x {self.urun.isim} (Sipariş #{self.siparis.id})"
    
    def kalem_toplam_getir(self):
        return self.adet * self.birim_fiyat