from rest_framework import serializers
from shopping_list.models import ProductToBuy

from .product_serializer import ProductSerializer


class ProductToBuySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductToBuy
        fields = ["id", "product"]
