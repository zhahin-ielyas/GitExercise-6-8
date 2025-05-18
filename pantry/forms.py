# forms.py
from django import forms
from .models import Ingredient, PantryItem

class PantryForm(forms.ModelForm):
    ingredient_name = forms.CharField(label='Ingredient Name')

    class Meta:
        model = PantryItem
        fields = ('ingredient_name', 'quantity', 'unit', 'storage_location', 'expiry_date')
