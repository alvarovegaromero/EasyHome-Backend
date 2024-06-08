from venv import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import Product
from utils.permissions.is_group_owner import IsGroupOwner

from ..serializers.product_serializer import ProductSerializer


class ProductUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def put(self, request, group_id, product_id):
        try:
            if "name" not in request.data or request.data["name"].strip() == "":
                return Response(
                    {"error": "The 'name' field is required."}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id, group_id=group_id)
            except Product.DoesNotExist:
                return Response({"error": "Product wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            product.name = request.data["name"].strip()
            product.save()

            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during product modification: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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
