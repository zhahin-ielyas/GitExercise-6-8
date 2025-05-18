from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),
    path('<str:category>/', views.ingredient_list, name='ingredient_list_by_category'),
    path('search/', views.search_ingredients, name='search_ingredients'),
    # Form to add new pantry item manually
    path('pantry/add/', views.add_pantry_item, name='add_pantry_item'),
    # Display item view
    path('item/<int:item_id>/', views.pantry_item_detail, name='pantry_item_detail'),
]