from django.contrib import admin
from .models import Ingredient, PantryItem, RecipeRating, MealPlan

admin.site.register(RecipeRating)
admin.site.register(Ingredient)
admin.site.register(PantryItem)
admin.site.register(MealPlan)

