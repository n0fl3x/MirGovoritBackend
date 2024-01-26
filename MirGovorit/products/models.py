from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        blank=False,
    )
    use_count = models.IntegerField(
        default=0,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.use_count} usages"

    def add_count(self) -> None:
        self.use_count += 1
        self.save()
