from django.test import Client, TestCase
from rest_framework import status

from groups.currency_choices import CURRENCY_CHOICES


class CurrenciesAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_currencies(self):
        response = self.client.get("/api/groups/currencies")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CURRENCY_CHOICES)
