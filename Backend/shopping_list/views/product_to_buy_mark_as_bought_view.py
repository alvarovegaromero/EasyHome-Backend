from decimal import Decimal, InvalidOperation
from venv import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.models import Product, ProductBought, ProductToBuy
from utils.permissions.is_group_member import IsGroupMember


def validate_price(price):  # TODO: move to is_valid from serializer
    try:
        price = Decimal(str(price))
    except InvalidOperation:
        return False, "Price must be a number"

    if price <= 0:
        return False, "Price must be positive"

    if price != round(price, 2):
        return False, "Price can have at most 2 decimal places"

    if len(str(price).replace(".", "")) > 7:
        return False, "Price can have at most 7 digits in total"

    return True, ""


class ProductToBuyMarkAsBoughtAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def post(self, request, group_id, product_id):
        try:
            price = request.data.get("price")

            if price is None or price == "":
                return Response(
                    {"error": "Missing price of the product bought"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            is_valid, error = validate_price(price)
            if not is_valid:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
                product_to_buy = product.purchase_intentions
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with id {product_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except ProductToBuy.DoesNotExist:
                return Response(
                    {"error": f"No ProductToBuy associated with Product id {product_id}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            ProductBought.objects.create(product=product, price=Decimal(price), user=request.user)

            product_to_buy.delete()

            return Response(
                {"message": "Product marked as bought successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(
                "An error occurred during retrieval of products marked to buy: %s" % str(e)
            )
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
