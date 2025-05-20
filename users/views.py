from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm  # Your custom register form
from pantry.models import PantryItem  # Your pantry model

@login_required
def dashboard(request):
    today = date.today()
    soon_threshold = today + timedelta(days=7)  # Items expiring within 7 days

    # Filter pantry items for the current user
    user_items = PantryItem.objects.filter(user=request.user)

    expired_items = user_items.filter(expiry_date__lt=today)
    expiring_today = user_items.filter(expiry_date=today)
    expiring_soon = user_items.filter(expiry_date__gt=today, expiry_date__lte=soon_threshold)

    context = {
        'expired_items': expired_items,
        'expiring_today': expiring_today,
        'expiring_soon': expiring_soon,
    }

    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})






