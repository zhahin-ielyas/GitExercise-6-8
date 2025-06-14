from django.contrib import admin
from .models import Ingredient
from .models import PantryItem
from .models import RecipeRating

admin.site.register(RecipeRating)
admin.site.register(Ingredient)
admin.site.register(PantryItem)

