from django.contrib.auth.models import User
from django.test import TestCase
from expense_distribution.models import Expense
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class GroupSettlementViewTest(TestCase):
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

    def test_get_settlement(self):
        response = self.client.get(f"/api/expense_distribution/{self.group.id}/settlements")

        settlements = Expense.getMinimumSettlements(Expense.objects.filter(group_id=self.group.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, settlements)

    def test_get_settlement_no_group(self):
        response = self.client.get(f"/api/expense_distribution/9999/settlements")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Group wasn't found"})

    def test_get_settlement_non_member(self):
        self.token = Token.objects.create(user=self.non_member)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(f"/api/expense_distribution/{self.group.id}/settlements")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "You are not a member of this group"})
