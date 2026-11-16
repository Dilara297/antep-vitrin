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