from django.contrib import admin
from django.urls import path

from products.views import add_product_to_recipe


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_product_to_recipe/', add_product_to_recipe, name="add_prod_to_rec"),
    # path('cook_recipe/', ), + recipe_id
    # path('show_recipes_without_product/', ), + product_id
]
