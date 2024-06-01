from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group

from ...models import Expense
from ...serializers.expenses_get_serializer import ExpensesGetSerializer


class ExpensesGetSerializerTest(TestCase):
    def test_expenses_get_serializer(self):
        # Create a User instance
        user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )

        group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=user,
        )

        # Create an Expense instance
        expense = Expense.objects.create(
            name="Test Expense",
            amount=100.00,
            paid_by=user,
            group=group,
        )

        # Serialize the Expense instance
        serializer = ExpensesGetSerializer(expense)

        # Check that the serialized data matches the expected result
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
