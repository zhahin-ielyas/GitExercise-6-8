"""
URL configuration for student_meal_plan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from users import views as user_views
from pantry import views
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.login_view, name='login'),       # Changed here: login URL is now /login/
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout_view, name='logout'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('pantry/', include('pantry.urls')),
    path('', RedirectView.as_view(url='/dashboard/')), 
]




