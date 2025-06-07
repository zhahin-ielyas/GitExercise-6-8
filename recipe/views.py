from django.shortcuts import render,redirect, get_object_or_404
import requests
from pantry.models import PantryItem,SavedRecipe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings


def recipe_list(request):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'number': 24,  # number of recipes per page
        'apiKey': settings.SPOONACULAR_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    recipes = data.get('results', [])

    return render(request, "recipe/recipe_list.html", {"recipes": recipes})



def search_recipe(request):
    query = request.GET.get('recipe_q', '')
    pantry_items = PantryItem.objects.filter(user=request.user)
    pantry_ingredients = set(item.ingredient.name.lower() for item in pantry_items)

    results = []

    if query:
        url = 'https://api.spoonacular.com/recipes/complexSearch'
        params = {
            'query': query,
            'number': 12,
            'addRecipeInformation': True,
            'fillIngredients': True,
            'apiKey': settings.SPOONACULAR_API_KEY,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for recipe in data.get('results', []):
                ingredients = recipe.get('extendedIngredients', [])

                recipe_ingredients = [i.get('name', '').lower() for i in ingredients]

                have = [i for i in recipe_ingredients if i in pantry_ingredients]
                missing = [i for i in recipe_ingredients if i not in pantry_ingredients]

                recipe['have_ingredients'] = have
                recipe['missing_ingredients'] = missing

                results.append(recipe)
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

