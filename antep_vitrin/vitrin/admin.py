from django.contrib import admin
from .models import Kategori, Urun

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('isim',)}

@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    list_display = ('isim', 'kategori', 'fiyat', 'stokta_var')
    list_filter = ('kategori', 'stokta_var')
    prepopulated_fields = {'slug': ('isim',)}