from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name="recipe_list"),
    path('search/', views.search_recipe, name='search_recipe'),
    path('save_recipe/', views.save_recipe, name='save_recipe'),
    path('saved_recipes/', views.view_saved_recipes, name='view_saved_recipes'),
    path('recipe/delete/<int:item_id>/', views.delete_recipe, name='delete_recipe'),
]
