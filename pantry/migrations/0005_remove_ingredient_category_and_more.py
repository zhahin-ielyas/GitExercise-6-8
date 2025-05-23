# Generated by Django 5.2 on 2025-05-12 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0004_remove_ingredient_default_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='default_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='default_unit',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pantry_images/'),
        ),
        migrations.AddField(
            model_name='pantryitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pantry_images/'),
        ),
    ]
