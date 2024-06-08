from venv import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import Product
from utils.permissions.is_group_owner import IsGroupOwner


class ProductUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def put(self, request, group_id, product_id):
        pass

    def delete(self, request, group_id, product_id):
        try:
            try:
                product = Product.objects.get(id=product_id, group_id=group_id)
            except Product.DoesNotExist:
                return Response({"error": "Product wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error("An error occurred during product deletion: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
