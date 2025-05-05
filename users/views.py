# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# View for register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After successful register, redirect to login page
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# View for logout
def logout_view(request):
    logout(request)
    return redirect('login')  # 👈 You can redirect to login or homepage

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
