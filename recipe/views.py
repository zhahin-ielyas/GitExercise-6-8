from django.shortcuts import render,redirect, get_object_or_404
import requests
from pantry.models import PantryItem,SavedRecipe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings


def recipe_list(request):
    url = f"https://api.spoonacular.com/recipes/informationBulk"
    params = {
        "includeNutrition": False,
        "apiKey": settings.SPOONACULAR_API_KEY,
    }
    response = requests.get(url, params=params)
    recipe = response.json()

    return render(request, "recipe/recipe_list.html", {"recipe": recipe})


def search_recipe(request):
    query = request.GET.get('q', '')
    pantry_items = PantryItem.objects.filter(user=request.user)  # if pantry is user-specific
    ingredient_list = ",".join(item.ingredient.name for item in pantry_items)
    results = []

    if query:
        print(f"DEBUG: Searching for '{query}'")
        url = 'https://api.spoonacular.com/recipes/complexSearch'
        params = {
            'query': query,
            'includeIngredients': ingredient_list,
            'fillIngredients': True,
            'number': 15,
            'apiKey': settings.SPOONACULAR_API_KEY,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
        else:
            print("API error:", response.status_code, response.text)

    return render(request, 'recipe/search_recipe.html', {
        'query': query,
        'results': results
    })

@login_required
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

@login_required
def view_saved_recipes(request):
    saved = SavedRecipe.objects.filter(user=request.user)
    return render(request, 'recipe/saved_recipes.html', {'saved_recipes': saved})

@login_required
def delete_recipe(request, item_id):
    recipe = get_object_or_404(SavedRecipe, id=item_id, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('view_saved_recipes')
    return render(request, 'recipe/delete_recipe.html', {'recipe': recipe})
