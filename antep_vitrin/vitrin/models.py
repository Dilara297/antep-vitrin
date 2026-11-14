from django.db import models

class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="URL'de görünecek isim (Örn: biber-salcasi)")

    class Meta:
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.isim

class Urun(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='urunler')
    isim = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    aciklama = models.TextField(blank=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    gorsel = models.ImageField(upload_to='urunler/')
    stokta_var = models.BooleanField(default=True)
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return self.isim