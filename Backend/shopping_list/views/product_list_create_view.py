from venv import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import Product
from utils.permissions.is_group_member import IsGroupMember

from ..serializers.product_serializer import ProductSerializer


class ProductListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        try:
            products = Product.objects.filter(group_id=group_id)

            serializer = ProductSerializer(products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during products retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, group_id):
        try:
            if "name" not in request.data or request.data["name"].strip() == "":
                return Response(
                    {"error": "The 'name' field is required."}, status=status.HTTP_400_BAD_REQUEST
                )

            product = Product.objects.create(name=request.data["name"].strip(), group_id=group_id)

            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("An error occurred during product creation: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
