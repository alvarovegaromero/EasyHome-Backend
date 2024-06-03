from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group, UserGroup

from ...models import Expense
from ...serializers.expense_detail_serializer import ExpenseDetailSerializer


class ExpenseDetailSerializerTest(TestCase):
    def test_expense_detail_serializer(self):
        user1 = User.objects.create_user(
            username="testuser1", email="testuser1@test.com", password="testpassword1"
        )

        user2 = User.objects.create_user(
            username="testuser2", email="testuser2@test.com", password="testpassword2"
        )

        user3 = User.objects.create_user(
            username="testuser3", email="testuser3@test.com", password="testpassword3"
        )

        group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=user1,
        )

        UserGroup.objects.create(user=user2, group=group)
        UserGroup.objects.create(user=user3, group=group)

        expense = Expense.objects.create(
            name="Test Expense",
            amount=100.00,
            paid_by=user1,
            group=group,
            date_paid=datetime.strptime("2021-01-01", "%Y-%m-%d").date(),
        )
        expense.debtors.add(user2)

        expense2 = Expense.objects.create(
            name="Test Expense 2",
            amount=200.00,
            paid_by=user2,
            group=group,
        )
        expense2.debtors.add(user1, user2, user3)

        serializer = ExpenseDetailSerializer(expense)

        self.assertEqual(
            serializer.data,
            {
                "id": expense.id,
                "name": "Test Expense",
                "amount": "100.00",
                "date_paid": "2021-01-01",
                "debtors": [{"id": user2.id, "username": user2.username}],
                "paid_by": {"id": user1.id, "username": user1.username},
                "group": group.id,
                "date_added": expense.date_added.strftime("%Y-%m-%d"),
            },
        )

        serializer2 = ExpenseDetailSerializer(expense2)

        self.assertEqual(
            serializer2.data,
            {
                "id": expense2.id,
                "name": "Test Expense 2",
                "amount": "200.00",
                "date_paid": expense2.date_paid.strftime("%Y-%m-%d"),
                "debtors": [
                    {"id": user1.id, "username": user1.username},
                    {"id": user2.id, "username": user2.username},
                    {"id": user3.id, "username": user3.username},
                ],
                "paid_by": {"id": user2.id, "username": user2.username},
                "group": group.id,
                "date_added": expense2.date_added.strftime("%Y-%m-%d"),
            },
        )
