from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),
    path('<str:category>/', views.ingredient_list, name='ingredient_list_by_category'),
    # Form view
    path('pantry/item/new/', views.pantry_item_new, name='pantry_item_new_form'),

# Display item view
    path('pantry/item/<str:name>/<int:quantity>/<str:unit>/<str:location>/<str:expiry>/', views.pantry_item_detail, name='pantry_item_detail'),
    # urls.py
    path('pantry/item/new/', views.pantry_item_new, name='pantry_item_new_form'),

]