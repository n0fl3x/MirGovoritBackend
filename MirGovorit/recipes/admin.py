from django.contrib import admin

from .models import Recipe, RecipeProducts


class RecipeProductInline(admin.TabularInline):
    model = RecipeProducts
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]


admin.site.register(Recipe, RecipeAdmin)
