from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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
    prod_amount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(limit_value=0)],
    )

    def save(self, *args, **kwargs) -> None:
        if self.prod_amount < 0:
            raise ValidationError(
                _(message="Amount of product can not be negative %(amount)s."),
                params={"amount": self.prod_amount},
                code="Invalid",
            )

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("recipe", "product")
