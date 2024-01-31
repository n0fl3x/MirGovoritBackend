from django.contrib import admin
from django.urls import path

from products.views import add_product_to_recipe, show_recipes_without_product
from recipes.views import cook_recipe


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_product_to_recipe/', add_product_to_recipe),
    path('cook_recipe/', cook_recipe),
    path('show_recipes_without_product/', show_recipes_without_product),
]
