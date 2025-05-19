from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm  # Make sure you have a form named RegisterForm in forms.py
from datetime import date, timedelta

# Import PantryItem model for expiry alerts
from pantry.models import PantryItem


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    today = date.today()
    soon = today + timedelta(days=3)

    # Expired items (before today)
    expired_items = PantryItem.objects.filter(
        user=request.user,
        expiry_date__lt=today,
        expiry_date__isnull=False
    )

    # Expiring today
    expiring_today = PantryItem.objects.filter(
        user=request.user,
        expiry_date=today
    )

    # Expiring in the next 1–3 days
    expiring_soon = PantryItem.objects.filter(
        user=request.user,
        expiry_date__gt=today,
        expiry_date__lte=soon
    )

    context = {
        'expired_items': expired_items,
        'expiring_today': expiring_today,
        'expiring_soon': expiring_soon,
    }

    return render(request, 'dashboard.html', context)




