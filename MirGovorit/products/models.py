from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )
    use_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name} - {self.use_count} usages"
