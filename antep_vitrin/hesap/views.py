from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def kayit_ol(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Kayıt olanı otomatik giriş yaptır
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
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
        
    return render(request, 'hesap/giris.html', {'form': form})

def cikis_yap(request):
    logout(request)
    return redirect('/')