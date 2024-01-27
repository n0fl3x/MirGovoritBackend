from pprint import pprint
from django.http import HttpResponse

from products.models import Product
from recipes.models import RecipeProducts, Recipe


def add_product_to_recipe(request):
    """
    Параметры: recipe_id, product_id, weight.

    Функция добавляет к указанному рецепту указанный продукт с указанным весом.
    Если в рецепте уже есть такой продукт, то функция должна поменять его вес в этом рецепте на указанный.
    """

    query_dict = request.GET.dict()

    try:
        rec_id = int(query_dict['recipe_id'])
        prod_id = int(query_dict['product_id'])
        weight = int(query_dict['weight'])
    except KeyError as k_er:
        return HttpResponse(f"Missing query parameter: {k_er}.")
    except ValueError as v_er:
        return HttpResponse(f"Invalid query parameter: {v_er}. Should be an integer.")

    rec_with_prod = RecipeProducts.objects.filter(
        recipe=rec_id,
        product=prod_id,
    )

    if rec_with_prod.exists():
        rec_with_prod.update(prod_amount=weight)
    else:
        cur_rec = Recipe.objects.filter(id=rec_id)
        cur_prod = Product.objects.filter(id=prod_id)

        if cur_rec.exists() and cur_prod.exists():
            RecipeProducts.objects.create(
                recipe=cur_rec[0],
                product=cur_prod[0],
                prod_amount=weight,
            )
        elif not cur_rec.exists() and cur_prod.exists():
            return HttpResponse(f"No such recipe with id {rec_id}.")
        elif cur_rec.exists() and not cur_prod.exists():
            return HttpResponse(f"No such product with id {prod_id}.")
        else:
            return HttpResponse(f"No such recipe with id {rec_id} and no such product with id {prod_id}.")

    return HttpResponse("Success!")
