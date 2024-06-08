from venv import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import ProductToBuy
from utils.permissions.is_group_member import IsGroupMember

from ..serializers.product_to_buy_serializer import ProductToBuySerializer


class ProductToBuyListAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        try:
            products_to_buy = ProductToBuy.objects.filter(product__group_id=group_id)

            serializer = ProductToBuySerializer(products_to_buy, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                "An error occurred during retrieval of products marked to buy: %s" % str(e)
            )
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
