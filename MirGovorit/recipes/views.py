from django.http import HttpResponse
from django.db.models import F

from products.models import Product
from .models import Recipe, RecipeProducts


def cook_recipe(request) -> HttpResponse:
    """
    Параметр: recipe_id.

    Функция увеличивает на единицу количество приготовленных блюд для каждого продукта,
    входящего в указанный рецепт.
    """

    query_dict = request.GET.dict()

    try:
        rec_id = int(query_dict['recipe_id'])
    except KeyError as k_er:
        return HttpResponse(f"Missing query parameter: {k_er}.")
    except ValueError as v_er:
        return HttpResponse(f"Invalid query parameter: {v_er}. Should be an integer.")

    cur_rec = Recipe.objects.filter(id=rec_id)

    if not cur_rec.exists():
        return HttpResponse(f"No such recipe with id = {rec_id}.")
    else:
        cur_rec_prods = RecipeProducts.objects.filter(recipe=rec_id).values_list("product")
        Product.objects.filter(id__in=cur_rec_prods).update(use_count=F('use_count') + 1)

    return HttpResponse("Success!")
