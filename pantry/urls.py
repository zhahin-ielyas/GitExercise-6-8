from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ingredient_list, {'category': None }, name='ingredient_list_all'),
    path('pantry/', views.ingredient_list, {'category': 'pantry' }, name='ingredient_list'),
    path('pantry/add/', views.add_pantry_item, name='add_pantry_item'),
    path('item/<int:item_id>/', views.pantry_item_detail, name='pantry_item_detail'),
    path('search-ingredient/', views.search_ingredients, name='search_ingredients'),
    path('pantry/edit/<int:item_id>/', views.edit_pantry_item, name='edit_pantry_item'),
    path('pantry/delete/<int:item_id>/', views.delete_pantry_item, name='delete_pantry_item'),
    path('generate-recipes/', views.generate_recipes, name='generate_recipes'),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path('select_ingredients/', views.select_ingredients, name='select_ingredients'),
    path('save_recipe/', views.save_recipe, name='save_recipe'),
    path('saved_recipes/', views.view_saved_recipes, name='view_saved_recipes'),
    path('recipe/delete/<int:item_id>/', views.delete_recipe, name='delete_recipe'),
    path('<str:category>/', views.ingredient_list, name='ingredient_list_by_category'),  
]

