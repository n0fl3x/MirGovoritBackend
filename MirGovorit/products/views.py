from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from products.models import Product
from recipes.models import RecipeProducts, Recipe


def add_product_to_recipe(request) -> HttpResponse:
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

    if weight < 0:
        return HttpResponse(f"Amount of product = {weight} is less then zero.")

    rec_with_prod = RecipeProducts.objects.filter(
        recipe=rec_id,
        product=prod_id,
    )

    if rec_with_prod.exists():
        rec_with_prod.update(prod_amount=weight)
    else:
        try:
            cur_rec = Recipe.objects.get(id=rec_id)
            cur_prod = Product.objects.get(id=prod_id)
        except ObjectDoesNotExist as er:
            return HttpResponse(er)

        RecipeProducts.objects.create(
            recipe=cur_rec,
            product=cur_prod,
            prod_amount=weight,
        )

    return HttpResponse("Success!")


def show_recipes_without_product(request) -> HttpResponse:
    """
    Параметр: product_id.

    Функция возвращает HTML страницу, на которой размещена таблица.
    В таблице отображены id и названия всех рецептов, в которых указанный продукт отсутствует,
    или присутствует в количестве меньше 10 грамм.
    """

    query_dict = request.GET.dict()

    try:
        prod_id = int(query_dict['product_id'])
    except KeyError as k_er:
        return HttpResponse(f"Missing query parameter: {k_er}.")
    except ValueError as v_er:
        return HttpResponse(f"Invalid query parameter: {v_er}. Should be an integer.")

    try:
        cur_prod = Product.objects.get(id=prod_id)
    except ObjectDoesNotExist as er:
        return HttpResponse(er)

    without_prod = Recipe.objects.exclude(products__exact=cur_prod.id)
    recipes_ids = RecipeProducts.objects.filter(product=cur_prod.id, prod_amount__lt=10). \
        select_related("recipe").values_list("recipe_id").distinct()
    ten_or_less = Recipe.objects.filter(id__in=recipes_ids)
    result_query = without_prod.union(ten_or_less)

    context = {"recipes_query": result_query}

    return render(
        request,
        template_name="recipes_list.html",
        context=context,
    )
