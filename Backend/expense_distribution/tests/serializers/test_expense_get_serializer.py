from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group

from ...models import Expense
from ...serializers.expenses_get_serializer import ExpensesGetSerializer


class ExpenseGetSerializerTest(TestCase):
    def test_expense_get_serializer(self):
        user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )

        group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=user,
        )

        expense = Expense.objects.create(
            name="Test Expense",
            amount=100.00,
            paid_by=user,
            group=group,
        )

        serializer = ExpensesGetSerializer(expense)

        self.assertEqual(
            serializer.data,
            {
                "id": expense.id,
                "name": "Test Expense",
                "amount": "100.00",
                "date_paid": expense.date_paid.isoformat().replace("+00:00", "Z"),
                "paid_by_username": "testuser",
            },
        )
