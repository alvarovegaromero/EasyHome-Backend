from venv import logger

from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import ProductBought
from utils.permissions.is_group_member import IsGroupMember

from ..serializers.product_bought_serializer import ProductBoughtSerializer


class ProductBoughtInRangeAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            user_id = request.query_params.get("user_id")  # Optional
            product_id = request.query_params.get("product_id")  # Optional

            if not start_date or not end_date:
                return Response(
                    {"error": "Both 'start_date' and 'end_date' are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if not start_date or not end_date:
                return Response(
                    {"error": "Invalid date format. Use 'YYYY-MM-DD'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if start_date > end_date:
                return Response(
                    {"error": "'start_date' must be before 'end_date'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            filters = {"product__group_id": group_id, "date__range": [start_date, end_date]}

            if user_id is not None:
                filters["user_id"] = user_id

            if product_id is not None:
                filters["product_id"] = product_id

            products_bought = ProductBought.objects.filter(**filters)

            serializer = ProductBoughtSerializer(products_bought, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                "An error occurred during retrieval of products bought in range: %s" % str(e)
            )
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
