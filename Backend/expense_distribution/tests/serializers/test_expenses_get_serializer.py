from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group, UserGroup

from ...models import Expense
from ...serializers.expenses_get_serializer import ExpensesGetSerializer


class ExpensesGetSerializerTest(TestCase):
    def test_expenses_get_serializer(self):
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
        )
        expense.debtors.add(user2)

        expense2 = Expense.objects.create(
            name="Test Expense 2",
            amount=200.00,
            paid_by=user2,
            group=group,
        )
        expense2.debtors.add(user1, user2, user3)

        serializer = ExpensesGetSerializer(group.get_expenses(), many=True)

        self.assertEqual(
            serializer.data,
            [
                {
                    "id": expense.id,
                    "name": "Test Expense",
                    "amount": "100.00",
                    "date_paid": expense.date_paid.isoformat().replace("+00:00", "Z"),
                    "paid_by_username": "testuser1",
                },
                {
                    "id": expense2.id,
                    "name": "Test Expense 2",
                    "amount": "200.00",
                    "date_paid": expense2.date_paid.isoformat().replace("+00:00", "Z"),
                    "paid_by_username": "testuser2",
                },
            ],
        )
