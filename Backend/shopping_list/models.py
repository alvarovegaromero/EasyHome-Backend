from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_current_date():
    return timezone.now().date()


class Product(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="group_products"
    )


class ProductToBuy(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="purchase_intentions"
    )


class ProductBought(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchases")
    date = models.DateField(default=get_current_date)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchased_products")
