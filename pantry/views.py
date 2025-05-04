from django.shortcuts import render
from . models import Ingredient
from . models import PantryItem
from .forms import PantryForm
from django.shortcuts import redirect

def base(request):
    return render(request, 'pantry/base.html')
def ingredient_list(request, category=None):
    if category:
        pantry_items = PantryItem.objects.filter(storage_location__iexact=category).order_by('expiry_date')
    else:
        pantry_items = PantryItem.objects.all().order_by('expiry_date')


    return render(request, 'pantry/ingredient_list.html', {'pantry_items': pantry_items,  'active_category': category or 'all',})
# Handles form submission
def pantry_item_new(request):
    if request.method == "POST":
        form = PantryForm(request.POST)
        if form.is_valid():
            ingredient_name = form.cleaned_data['ingredient_name']
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)

            item = form.save(commit=False)
            item.author = request.user
            item.save()
            return redirect('pantry_item_detail',
                name=item.ingredient.name,
                quantity=item.quantity,
                unit=item.unit,
                location=item.storage_location.title(),
                expiry=item.expiry_date.strftime('%Y-%m-%d') if item.expiry_date else "N/A"
            )
    else:
        form = PantryForm()
    return render(request, 'pantry/pantry_item_edit.html', {'form': form})


# Shows saved item from URL
def pantry_item_detail(request, name, quantity, unit, location, expiry):
    return render(request, 'pantry/pantry_item_detail.html', {
        'name': name,
        'quantity': quantity,
        'unit': unit,
        'location': location,
        'expiry': expiry
    })

   
# Create your views here.
