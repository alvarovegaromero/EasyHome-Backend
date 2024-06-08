from django.contrib.auth.models import User
from rest_framework import serializers
from shopping_list.models import ProductBought

from .product_serializer import ProductSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ProductBoughtSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductBought
        fields = ["id", "product", "user", "price", "date"]
