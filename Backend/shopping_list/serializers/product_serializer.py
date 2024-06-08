from rest_framework import serializers
from shopping_list.models import Product, ProductToBuy


class ProductSerializer(serializers.ModelSerializer):
    marked_to_buy = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "group", "marked_to_buy"]

    def get_marked_to_buy(self, obj):
        return ProductToBuy.objects.filter(product=obj).exists()
