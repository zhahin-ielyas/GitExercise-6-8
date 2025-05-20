import csv
from django.core.management.base import BaseCommand
from pantry.models import Ingredient

class Command(BaseCommand):
    help = 'Import ingredients from a CSV file'

    def handle(self, *args, **kwargs):
        with open('ingredients_malaysia.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row['name'],
                    defaults={
                        'category': row['category'],
                        'image_url': row['image_url'],
                        'default_unit': row['default_unit'],
                        'default_quantity': row['default_quantity'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported ingredients'))
