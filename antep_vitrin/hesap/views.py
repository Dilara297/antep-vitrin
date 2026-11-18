from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from sepet.models import Sepet, SepetUrunu, Siparis

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