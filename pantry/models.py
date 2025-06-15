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
    recipe_id = models.IntegerField()  
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    recipe_id = models.IntegerField()  
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class RecipeRating(models.Model):
    recipe_id = models.IntegerField()  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe_id', 'user')   