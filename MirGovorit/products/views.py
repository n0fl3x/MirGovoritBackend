from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
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

    rec_with_prod = RecipeProducts.objects.filter(
        recipe=rec_id,
        product=prod_id,
    )

    try:
        cur_rec_id = Recipe.objects.get(id=rec_id).id
        cur_prod_id = Product.objects.get(id=prod_id).id
    except ObjectDoesNotExist as er:
        return HttpResponse(er)

    if rec_with_prod.exists():
        rec_with_prod_id = rec_with_prod.first().id
        try:
            rec_with_prod.first().update_amount(
                rp_id=rec_with_prod_id,
                amount=weight,
            )
        except ValidationError as v_er:
            return HttpResponse(v_er)
    else:
        try:
            RecipeProducts.objects.create(
                recipe_id=cur_rec_id,
                product_id=cur_prod_id,
                prod_amount=weight,
            )
        except ValidationError as v_err:
            return HttpResponse(v_err)

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
        Product.objects.get(id=prod_id)
    except ObjectDoesNotExist as er:
        return HttpResponse(er)

    rec_ids = RecipeProducts.objects.filter(
        ~Q(product_id=prod_id) |
        (Q(product_id__exact=prod_id) & Q(prod_amount__lt=10))
    ).select_related("recipe").values_list("recipe_id").distinct()

    result_query = Recipe.objects.filter(id__in=rec_ids)

    context = {"recipes_query": result_query}

    return render(
        request,
        template_name="recipes_list.html",
        context=context,
    )
