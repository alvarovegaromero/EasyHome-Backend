from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group, UserGroup

from ...serializers.expense_creator_serializer import ExpenseCreatorSerializer


class ExpenseCreatorSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", email="testuser1@test.com", password="testpassword1"
        )

        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@test.com", password="testpassword2"
        )

        self.group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=self.user1,
        )

        UserGroup.objects.create(user=self.user2, group=self.group)

    def test_expense_creator_serializer(self):
        data = {
            "name": "Test Expense",
            "amount": "100.00",
            "debtors": [self.user2.id],
            "paid_by": self.user1.id,
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        expense = serializer.save()

        self.assertEqual(expense.name, "Test Expense")
        self.assertEqual(expense.amount, Decimal("100.00"))
        self.assertEqual(list(expense.debtors.all()), [self.user2])
        self.assertEqual(expense.paid_by, self.user1)
        self.assertEqual(expense.group, self.group)

    def test_expense_creator_serializer_without_name(self):
        data = {
            "amount": "100.00",
            "debtors": [self.user2.id],
            "paid_by": self.user1.id,
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["name"][0], "Name must be provided")

    def test_expense_creator_serializer_without_amount(self):
        data = {
            "name": "Test Expense",
            "debtors": [self.user2.id],
            "paid_by": self.user1.id,
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["amount"][0], "Amount must be provided")

    def test_expense_creator_serializer_with_amount_less_than_min_value(self):
        data = {
            "name": "Test Expense",
            "amount": "0",
            "debtors": [self.user2.id],
            "paid_by": self.user1.id,
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["amount"][0], "Amount must be greater than 0")

        data = {
            "name": "Test Expense",
            "amount": "-10",
            "debtors": [self.user2.id],
            "paid_by": self.user1.id,
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["amount"][0], "Amount must be greater than 0")

    def test_expense_creator_serializer_without_debtors(self):
        data = {
            "name": "Test Expense",
            "amount": "100.00",
            "paid_by": self.user1.id,
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["debtors"][0], "Debtors must be provided")

    def test_expense_creator_serializer_without_paid_by(self):
        data = {
            "name": "Test Expense",
            "amount": "100.00",
            "debtors": [self.user2.id],
            "group": self.group.id,
        }

        serializer = ExpenseCreatorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["paid_by"][0], "Paid_by must be provided")
