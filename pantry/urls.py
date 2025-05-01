from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),
    path('<str:category>/', views.ingredient_list, name='ingredient_list_by_category'),
]