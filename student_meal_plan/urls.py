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
from django.contrib.auth import views as auth_views  # add this at the top
from django.contrib import admin
from django.urls import path, include
# from users import views as user_views
from pantry import views
from django.http import HttpResponse

def simple_test_view(request):
    print("DEBUG: simple_test_view hit!")
    return HttpResponse("<h1>Simple test view works!</h1>")
urlpatterns = [
    path('simple-test/', simple_test_view),
    path('admin/', admin.site.urls),
    # path('register/', user_views.register, name='register'),
    # path('logout/', user_views.logout_view, name='logout'), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('dashboard/', user_views.dashboard, name='dashboard'),
    path('', include('pantry.urls')),
]

