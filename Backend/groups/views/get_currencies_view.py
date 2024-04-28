from rest_framework.views import APIView
from rest_framework.response import Response
from groups.currency_choices import CURRENCY_CHOICES

class CurrenciesAPIView(APIView):
    def get(self, request):
        return Response(CURRENCY_CHOICES)