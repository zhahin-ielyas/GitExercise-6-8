from django.contrib import admin
from .models import Ingredient
from .models import PantryItem

admin.site.register(Ingredient)
admin.site.register(PantryItem)
# Register your models here.
