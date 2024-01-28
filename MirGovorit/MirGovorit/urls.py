from django.contrib import admin
from django.urls import path

from products.views import add_product_to_recipe
from recipes.views import cook_recipe


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_product_to_recipe/', add_product_to_recipe, name="add_prod_to_rec"),
    path('cook_recipe/', cook_recipe, name="cook_rec"),
    # path('show_recipes_without_product/', ), + product_id
]
