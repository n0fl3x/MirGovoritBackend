from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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

    @classmethod
    def update_amount(cls, rp_id: int, amount: int):
        if amount < 0:
            raise ValidationError(message=f"Amount of product can not be negative ({amount}).")

        cls.objects.filter(pk=rp_id). \
            update(prod_amount=F("prod_amount") - F("prod_amount") + amount)

    def save(self, *args, **kwargs) -> None:
        if self.prod_amount < 0:
            raise ValidationError(message=f"Amount of product can not be negative ({self.prod_amount}).")
        super().save(*args, **kwargs)
