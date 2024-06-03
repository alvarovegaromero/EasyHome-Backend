from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from expense_distribution.models import Expense
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ...serializers.expense_detail_serializer import ExpenseDetailSerializer
from ...serializers.expenses_get_serializer import ExpensesGetSerializer


class GroupExpensesViewTest(TestCase):
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

    def test_get_expenses(self):
        response = self.client.get(f"/api/expense_distribution/{self.group.id}/expenses")

        group_expenses = ExpensesGetSerializer(self.group.get_expenses(), many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, group_expenses)

    def test_get_expenses_no_group(self):
        response = self.client.get(f"/api/expense_distribution/9999/expenses")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Group wasn't found"})

    def test_get_expenses_non_member(self):
        self.token = Token.objects.create(user=self.non_member)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(f"/api/expense_distribution/{self.group.id}/expenses")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "You are not a member of this group"})

    def test_post_expense(self):
        data = {
            "name": "Test Expense 2",
            "amount": 200.00,
            "paid_by": self.user1.id,
            "debtors": [self.user2.id],
        }
        response = self.client.post(
            f"/api/expense_distribution/{self.group.id}/expenses", data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data["expense"]["amount"]), Decimal(data["amount"]))
        self.assertEqual(response.data["expense"]["paid_by"]["id"], data["paid_by"])
        debtors_ids = [debtor["id"] for debtor in response.data["expense"]["debtors"]]
        self.assertEqual(debtors_ids, data["debtors"])

        expense = Expense.objects.get(name=data["name"])
        expense_serializer = ExpenseDetailSerializer(expense)
        self.assertEqual(response.data["expense"], expense_serializer.data)

    def test_post_expense_with_date(self):
        data = {
            "name": "Test Expense 2",
            "amount": 200.00,
            "paid_by": self.user1.id,
            "debtors": [self.user2.id],
            "date_paid": "2023-08-29",
        }

        response = self.client.post(
            f"/api/expense_distribution/{self.group.id}/expenses", data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data["expense"]["amount"]), Decimal(data["amount"]))
        self.assertEqual(response.data["expense"]["paid_by"]["id"], data["paid_by"])
        debtors_ids = [debtor["id"] for debtor in response.data["expense"]["debtors"]]
        self.assertEqual(debtors_ids, data["debtors"])
        self.assertEqual(response.data["expense"]["date_paid"], data["date_paid"])

        expense = Expense.objects.get(name=data["name"])
        expense_serializer = ExpenseDetailSerializer(expense)
        self.assertEqual(response.data["expense"], expense_serializer.data)

    def test_post_expense_no_group(self):
        data = {
            "name": "Test Expense 2",
            "amount": 200.00,
            "paid_by": self.user1.id,
            "debtors": [self.user2.id],
        }
        response = self.client.post(f"/api/expense_distribution/9999/expenses", data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Group wasn't found"})

    def test_post_expense_non_member(self):
        self.token = Token.objects.create(user=self.non_member)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "name": "Test Expense 2",
            "amount": 200.00,
            "paid_by": self.user1.id,
            "debtors": [self.user2.id],
        }
        response = self.client.post(
            f"/api/expense_distribution/{self.group.id}/expenses", data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "You are not a member of this group"})
