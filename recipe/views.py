from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib import messages
from django.conf import settings

from pantry.models import PantryItem, SavedRecipe, RecipeRating

import requests

def recipe_list(request):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'number': 24,  
        'apiKey': settings.SPOONACULAR_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    recipes = data.get('results', [])

    for recipe in recipes:
        rid = recipe['id']
        ratings = RecipeRating.objects.filter(recipe_id=rid)
        recipe['average_rating'] = ratings.aggregate(Avg('rating'))['rating__avg']
        recipe['rating_count'] = ratings.count()

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

                rid = recipe['id']
                ratings = RecipeRating.objects.filter(recipe_id=rid)
                recipe['average_rating'] = ratings.aggregate(Avg('rating'))['rating__avg']
                recipe['rating_count'] = ratings.count()


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
def submit_rating(request, recipe_id):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        rating_value = int(request.POST.get('rating'))
        source = request.GET.get('source')
        recipe_q = request.GET.get('recipe_q')

        existing_rating = RecipeRating.objects.filter(user=request.user, recipe_id=recipe_id).first()

        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
            messages.success(request, "Your rating has been updated.")
        else:
            RecipeRating.objects.create(
                user=request.user,
                recipe_id=recipe_id,
                rating=rating_value
            )
            messages.success(request, "Thanks for rating!")

        if source == "search" and recipe_q:
            return redirect(f'/recipe/{recipe_id}/?source=search&recipe_q={recipe_q}')
        elif source:
            return redirect(f'/recipe/{recipe_id}/?source={source}')
        else:
            return redirect('recipe_detail', recipe_id=recipe_id)

