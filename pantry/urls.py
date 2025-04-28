from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),
    path('', views.pantryItem_list, name='pantryItem_list'),
]