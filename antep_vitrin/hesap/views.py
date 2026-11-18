from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from sepet.models import Sepet, SepetUrunu, Siparis
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profil

def kayit_ol(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # login() session_key'i değiştirmeden önce yakalıyoruz
            eski_session_id = request.session.session_key
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        
    return render(request, 'hesap/kayit.html', {'form': form})

def giris_yap(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login() session_key'i değiştirmeden önce yakalıyoruz
            eski_session_id = request.session.session_key
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
        
    return render(request, 'hesap/giris.html', {'form': form})

def cikis_yap(request):
    logout(request)
    return redirect('/')

@login_required(login_url='giris_yap')
def profil(request):
    profil_obj, _ = Profil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        
        profil_obj.telefon = request.POST.get('telefon', '').strip()
        profil_obj.adres = request.POST.get('adres', '').strip()
        profil_obj.save()
        
        messages.success(request, 'Profil bilgileriniz başarıyla güncellendi.')
        return redirect('profil')
        
    tamamlanan_siparisler = Siparis.objects.filter(
        user=request.user, 
        kargo_durumu='Teslim Edildi'
    ).order_by('-olusturulma_tarihi')
    
    return render(request, 'hesap/profil.html', {
        'profil': profil_obj,
        'tamamlanan_siparisler': tamamlanan_siparisler
    })