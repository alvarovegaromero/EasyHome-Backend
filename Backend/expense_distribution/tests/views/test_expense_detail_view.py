from django.contrib.auth.models import User
from django.test import TestCase
from expense_distribution.models import Expense
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ...serializers.expense_detail_serializer import ExpenseDetailSerializer


class ExpenseDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")
        self.non_member = User.objects.create_user(username="nonmember", password="testpass")

        self.group = Group.objects.create(name="Test Group", currency="EUR", owner=self.user1)
        UserGroup.objects.create(user=self.user2, group=self.group)

        self.expense = Expense.objects.create(
            name="Test Expense", amount=100.00, paid_by=self.user1, group=self.group
        )
        self.expense.debtors.add(self.user2)
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_expense(self):
        response = self.client.get(
            f"/api/expense_distribution/{self.group.id}/expenses/{self.expense.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ExpenseDetailSerializer(self.expense).data)

    def test_get_expense_no_group(self):
        response = self.client.get(f"/api/expense_distribution/9999/expenses/{self.expense.id}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Group wasn't found"})

    def test_get_expense_non_member(self):
        self.token = Token.objects.create(user=self.non_member)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(
            f"/api/expense_distribution/{self.group.id}/expenses/{self.expense.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "You are not a member of this group"})

    def test_get_expense_no_expense(self):
        response = self.client.get(f"/api/expense_distribution/{self.group.id}/expenses/9999")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Expense wasn't found"})

    def test_delete_expense(self):
        response = self.client.delete(
            f"/api/expense_distribution/{self.group.id}/expenses/{self.expense.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(id=self.expense.id)

    def test_delete_expense_no_group(self):
        response = self.client.delete(f"/api/expense_distribution/9999/expenses/{self.expense.id}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Group wasn't found"})

    def test_delete_expense_non_member(self):
        self.token = Token.objects.create(user=self.non_member)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.delete(
            f"/api/expense_distribution/{self.group.id}/expenses/{self.expense.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "You are not a member of this group"})

    def test_delete_expense_no_expense(self):
        response = self.client.delete(f"/api/expense_distribution/{self.group.id}/expenses/9999")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Expense wasn't found"})
