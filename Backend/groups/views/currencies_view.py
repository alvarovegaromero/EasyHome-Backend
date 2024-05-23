from venv import logger

from groups.currency_choices import CURRENCY_CHOICES
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CurrenciesAPIView(APIView):
    def get(self, request):
        try:
            return Response(CURRENCY_CHOICES)
        except Exception as e:
            logger.error(
                "An error occurred during currencies retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
