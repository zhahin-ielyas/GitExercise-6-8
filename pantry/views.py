from django.shortcuts import render,redirect, get_object_or_404
from . models import Ingredient, PantryItem
from .forms import PantryForm

def base(request):
    return render(request, 'pantry/base.html')
def ingredient_list(request, category=None):
    if category:
        pantry_items = PantryItem.objects.filter(storage_location__iexact=category).order_by('expiry_date')
    else:
        pantry_items = PantryItem.objects.all().order_by('expiry_date')


    return render(request, 'pantry/ingredient_list.html', {'pantry_items': pantry_items,  'active_category': category or 'all',})

def search_ingredients(request):
    return render(request, 'pantry/search_ingredients.html', {'active_category': 'search'})

# Updated function: handles both search add + form add
def add_pantry_item(request):
    if request.method == 'POST':
        form = PantryForm(request.POST)
        if form.is_valid():
            ingredient_name = form.cleaned_data['ingredient_name']

            # Create the Ingredient object
            ingredient = Ingredient.objects.create(
                name=ingredient_name,
                default_quantity=form.cleaned_data['quantity'],
                default_unit=form.cleaned_data['unit']
            )

            # Create the PantryItem and assign the new ingredient
            pantry_item = form.save(commit=False)
            pantry_item.user = request.user
            pantry_item.ingredient = ingredient
            pantry_item.save()

            return redirect('ingredient_list')
    else:
        form = PantryForm()

    return render(request, 'pantry/add_pantry_item.html', {'form': form})

# Shows saved item from URL
def pantry_item_detail(request, item_id):
    item = get_object_or_404(PantryItem, id=item_id)
    return render(request, 'pantry/pantry_item_detail.html', {
        'name': item.ingredient.name,
        'quantity': item.quantity,
        'unit': item.unit,
        'location': item.storage_location,
        'expiry': item.expiry_date,
        'image': item.ingredient.image.url if item.ingredient.image else None
    })


   
# Create your views here.
