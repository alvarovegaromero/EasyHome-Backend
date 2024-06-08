from venv import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import Product, ProductToBuy
from utils.permissions.is_group_member import IsGroupMember

from ..serializers.product_to_buy_serializer import ProductToBuySerializer


class ProductMarkToBuyAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def post(self, request, group_id, product_id):
        try:
            try:
                product = Product.objects.get(id=product_id, group_id=group_id)
            except Product.DoesNotExist:
                return Response({"error": "Product wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            if ProductToBuy.objects.filter(product=product).exists():
                return Response(
                    {"error": "Product is already marked to buy"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product_to_buy = ProductToBuy.objects.create(product=product)

            return Response(
                ProductToBuySerializer(product_to_buy).data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error("An error occurred during marking product as to buy: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
