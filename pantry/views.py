from django.shortcuts import render

def ingredient_list(request):
    return render(request, 'pantry/ingredient_list.html', {})
def pantryItem_list(request):
    return render(request, 'pantry/pantryItem_list.html', {})
# Create your views here.
