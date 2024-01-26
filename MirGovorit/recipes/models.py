from django.db import models, IntegrityError

from products.models import Product


class Recipe(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        blank=False,
    )
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
    prod_amount = models.IntegerField(
        default=0,
        null=False,
        blank=False,
    )

    def save(self, *args, **kwargs) -> None:
        result = RecipeProducts.objects.filter(recipe=self.recipe, product=self.product)
        if not result.exists():
            super(RecipeProducts, self).save(*args, **kwargs)
        else:
            amount = result[0].prod_amount
            raise IntegrityError(f"This recipe already contains this product in amount of {amount}")
