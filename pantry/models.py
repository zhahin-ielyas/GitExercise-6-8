from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class PantryItem(models.Model):
    STORAGE_CHOICES = [
        ('pantry', 'Pantry'),
        ('fridge', 'Fridge'),
        ('freezer', 'Freezer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)  
    storage_location = models.CharField(max_length=10, choices=STORAGE_CHOICES)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} ({self.storage_location})"



