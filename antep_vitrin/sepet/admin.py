from django.contrib import admin
from .models import Sepet, SepetUrunu, Siparis, SiparisUrunu

class SiparisUrunuInline(admin.TabularInline):
    model = SiparisUrunu
    extra = 0
    readonly_fields = ('urun', 'adet', 'birim_fiyat')

@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'odenen_tutar', 'kargo_durumu', 'kargo_takip_no', 'olusturulma_tarihi')
    list_filter = ('kargo_durumu', 'olusturulma_tarihi')
    list_editable = ('kargo_durumu', 'kargo_takip_no')
    inlines = [SiparisUrunuInline]

admin.site.register(Sepet)
admin.site.register(SepetUrunu)
