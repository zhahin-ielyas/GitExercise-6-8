import requests
from django.shortcuts import render,redirect, get_object_or_404
from . models import Ingredient, PantryItem, SavedRecipe
from .forms import PantryForm
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST

print("== pantry/views.py loaded ==")

import requests
from django.conf import settings

def fetch_image_from_spoonacular(ingredient_name):
    try:
        response = requests.get(
            'https://api.spoonacular.com/food/ingredients/search',
            params={
                'query': ingredient_name,
                'apiKey': settings.SPOONACULAR_API_KEY
            }
        )
        data = response.json()
        if data['results']:
            image_path = data['results'][0]['image']
            return f"https://spoonacular.com/cdn/ingredients_250x250/{image_path}"
    except Exception as e:
        print(f"Error fetching image for '{ingredient_name}':", e)
    return None  # fallback if API fails or empty

def base(request):
    return render(request, 'pantry/base.html')
def ingredient_list(request, category=None):
    if category:
        pantry_items = PantryItem.objects.filter(storage_location__iexact=category).order_by('expiry_date')
    else:
        pantry_items = PantryItem.objects.all().order_by('expiry_date')


    return render(request, 'pantry/ingredient_list.html', {'pantry_items': pantry_items,  'active_category': category or 'all',})

def search_ingredients(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        print(f"DEBUG: Searching for '{query}'")
        url = 'https://api.spoonacular.com/food/ingredients/search'
        params = {
            'query': query,
            'number': 15,
            'apiKey': settings.SPOONACULAR_API_KEY,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
        else:
            print("API error:", response.status_code, response.text)

    return render(request, 'pantry/search_ingredients.html', {
        'query': query,
        'results': results
    })
# Updated function: handles both search add + form add
def add_pantry_item(request):
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        image_url = request.POST.get('image_url')  # optional input
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')
        location = request.POST.get('storage_location')
        expiry_input = request.POST.get('expiry_date')

        expiry = expiry_input.strip() if expiry_input else None
        if expiry and expiry.lower() == 'n/a':
            expiry = None

        ingredient, created = Ingredient.objects.get_or_create(
            name__iexact=ingredient_name,
            defaults={"name": ingredient_name}
        )

        # Fetch image if newly created and no image provided
        if created or not ingredient.image_url:
            image_url = fetch_image_from_spoonacular(ingredient_name)
            if image_url:
                ingredient.image_url = image_url
                ingredient.save()

        PantryItem.objects.create(
            user=request.user,
            ingredient=ingredient,
            quantity=quantity,
            unit=unit,
            storage_location=location,
            expiry_date=expiry
        )
        return redirect('ingredient_list')

    return render(request, 'pantry/add_pantry_item.html')

# Shows saved item from URL
def pantry_item_detail(request, item_id):
    item = get_object_or_404(PantryItem, id=item_id)
    return render(request, 'pantry/pantry_item_detail.html', {
        'name': item.ingredient.name,
        'quantity': item.quantity,
        'unit': item.unit,
        'location': item.storage_location,
        'expiry': item.expiry_date,
        'image': item.ingredient.image_url if item.ingredient.image_url else None
    })

def edit_pantry_item(request, item_id):
    item = get_object_or_404(PantryItem, id=item_id)

    if request.method == 'POST':
        item.quantity = request.POST.get('quantity')
        item.unit = request.POST.get('unit')
        item.storage_location = request.POST.get('storage_location')
        item.expiry_date = request.POST.get('expiry_date')
        item.save()
        return redirect('ingredient_list')  

    return render(request, 'pantry/edit_pantry_item.html', {'item': item})


def delete_pantry_item(request, item_id):
    item = get_object_or_404(PantryItem, id=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('ingredient_list')  

    return render(request, 'pantry/delete_pantry_item.html', {'item': item})

def generate_recipes(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('ingredients')  # list of PantryItem IDs
        pantry_items = PantryItem.objects.filter(id__in=selected_ids, user=request.user)
    else:
        pantry_items = PantryItem.objects.filter(user=request.user)

    ingredients = ",".join([item.ingredient.name for item in pantry_items])

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 15,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": settings.SPOONACULAR_API_KEY,
    }

    response = requests.get(url, params=params)
    recipes = response.json()

    return render(request, "pantry/recipe_results.html", {"recipes": recipes})

def recipe_detail(request, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "includeNutrition": False,
        "apiKey": settings.SPOONACULAR_API_KEY,
    }
    response = requests.get(url, params=params)
    recipe = response.json()

    return render(request, "pantry/recipe_detail.html", {"recipe": recipe})

def select_ingredients(request):
    pantry_items = PantryItem.objects.filter(user=request.user)

    return render(request, 'pantry/select_ingredients.html', {
        'pantry_items': pantry_items
    })

def save_recipe(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        title = request.POST.get('title')
        image = request.POST.get('image')

        # Avoid saving duplicate recipes
        exists = SavedRecipe.objects.filter(user=request.user, recipe_id=recipe_id).exists()
        if not exists:
            SavedRecipe.objects.create(
                user=request.user,
                title=title,
                image=image,
                recipe_id=recipe_id
            )

        return redirect('view_saved_recipes')  
    
def view_saved_recipes(request):
    saved = SavedRecipe.objects.filter(user=request.user)
    return render(request, 'pantry/saved_recipes.html', {'saved_recipes': saved})
