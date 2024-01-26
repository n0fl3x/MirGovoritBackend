from django.contrib import admin

from .models import Recipe, RecipeProducts


admin.site.register(Recipe)
admin.site.register(RecipeProducts)
