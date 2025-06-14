from django.db import models
from django.contrib.auth.models import User

DAYS = [
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
]

MEALS = [
    ("Breakfast", "Breakfast"),
    ("Snack1", "Snack - 1"),
    ("Lunch", "Lunch"),
    ("Snack2", "Snack - 2"),
    ("Dinner", "Dinner"),
]

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    default_quantity = models.FloatField(null=True, blank=True)
    default_unit = models.CharField(max_length=20, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True) 
    
    def __str__(self):
        return self.name

class PantryItem(models.Model):   
    STORAGE_CHOICES = [
        ('pantry', 'Pantry'),
        ('fridge', 'Fridge'),
        ('freezer', 'Freezer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    storage_location = models.CharField(max_length=10, choices=STORAGE_CHOICES)
    expiry_date = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} ({self.storage_location})"

    def get_default_quantity(self):
        return self.ingredient.default_quantity

    def get_default_unit(self):
        return self.ingredient.default_unit
    
class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    recipe_id = models.IntegerField()  # Spoonacular recipe ID
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
        
class MealPlan (models.Model):
    meal_type = models.CharField(max_length=10, choices=MEALS)
    day = models.CharField(max_length=3, choices=DAYS)
    food = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.meal_type} - {self.day}: {self.food}"
