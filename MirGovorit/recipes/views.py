from django.http import HttpResponse, HttpRequest
from django.db.models import F
from django.views.decorators.http import require_GET

from products.models import Product
from .models import Recipe, RecipeProducts


@require_GET
def cook_recipe(request: HttpRequest) -> HttpResponse:
    """
    Параметр: recipe_id.

    Функция увеличивает на единицу количество приготовленных блюд для каждого продукта,
    входящего в указанный рецепт.
    """

    query_dict = request.GET.dict()
    try:
        rec_id = int(query_dict['recipe_id'])
    except KeyError as k_er:
        return HttpResponse(
            content=f"Missing query parameter: {k_er}.",
            status=400,
        )
    except ValueError as v_er:
        return HttpResponse(
            content=f"Invalid query parameter: {v_er}. Should be an integer.",
            status=400,
        )

    cur_rec = Recipe.objects.filter(id=rec_id)
    if not cur_rec.exists():
        return HttpResponse(
            content=f"No such recipe with id = {rec_id}.",
            status=500,
        )
    else:
        cur_rec_prods = RecipeProducts.objects.filter(recipe=rec_id).values_list("product")
        Product.objects.filter(id__in=cur_rec_prods).update(use_count=F('use_count') + 1)

    return HttpResponse(
        content="Success!",
        status=200,
    )
