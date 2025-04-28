from django.shortcuts import render
from . models import Ingredient
from . models import PantryItem

def ingredient_list(request):
    ingredients=Ingredient.objects.all() 
    return render(request, 'pantry/ingredient_list.html', {'ingredients': ingredients})
def pantryItem_list(request):
    pantryItem= PantryItem.objects.order_by('expiry_date')
    return render(request, 'pantry/pantryItem_list.html', {'pantryItem': pantryItem})
# Create your views here.
