from django.urls import path
from . import views
from .views import submit_rating

urlpatterns = [
    path('', views.recipe_list, name="recipe_list"),
    path('search/', views.search_recipe, name='search_recipe'),
    
]
