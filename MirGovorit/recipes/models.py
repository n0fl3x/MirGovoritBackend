from django.db import models

from products.models import Product


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(
        to=Product,
        through='RecipeProducts',
    )

    def __str__(self) -> str:
        return f"{self.name}"


class RecipeProducts(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
    )
    prod_amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs) -> None:
        result = RecipeProducts.objects.filter(
            recipe=self.recipe,
            product=self.product
        )
        if not result.exists():
            super(RecipeProducts, self).save(*args, **kwargs)
        else:
            obj = result[0]
            amount = obj.prod_amount

            if self.prod_amount != amount:
                result.update(prod_amount=self.prod_amount)
