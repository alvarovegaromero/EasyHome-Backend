from django.contrib.auth.models import User
from django.test import TestCase
from expense_distribution.models import Expense
from groups.models import Group, UserGroup


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", email="testuser1@test.com", password="testpassword1"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@test.com", password="testpassword2"
        )
        self.user3 = User.objects.create_user(
            username="testuser3", email="testuser3@test.com", password="testpassword3"
        )
        self.user4 = User.objects.create_user(
            username="testuser4", email="testuser4@test.com", password="testpassword4"
        )

        self.group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=self.user1,
        )

        UserGroup.objects.create(user=self.user2, group=self.group)
        UserGroup.objects.create(user=self.user3, group=self.group)
        UserGroup.objects.create(user=self.user4, group=self.group)

    def test_get_minimum_settlements_with_no_expenses(self):
        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 0)

    def test_get_minimum_settlements_with_one_shared_expense(self):
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=300,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user1, self.user2, self.user3)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 2)
        self.assertIn(
            {"payer": self.user2.id, "receiver": self.user1.id, "amount": "100.00"}, transactions
        )
        self.assertIn(
            {"payer": self.user3.id, "receiver": self.user1.id, "amount": "100.00"}, transactions
        )

    def test_get_minimum_settlements_with_one_expense_and_one_debtor(self):
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=300,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user2)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 1)
        self.assertIn(
            {"payer": self.user2.id, "receiver": self.user1.id, "amount": "300.00"}, transactions
        )

    def test_get_minimum_settlements_with_multiple_expenses_and_multiple_debtors(self):
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=300,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user2, self.user3)

        expense2 = Expense.objects.create(
            name="Expense 2",
            amount=200,
            group=self.group,
            paid_by=self.user2,
        )
        expense2.debtors.add(self.user1, self.user3)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 2)
        self.assertIn(
            {"payer": self.user3.id, "receiver": self.user1.id, "amount": "200.00"}, transactions
        )
        self.assertIn(
            {"payer": self.user3.id, "receiver": self.user2.id, "amount": "50.00"}, transactions
        )

    def test_get_minimum_settlements_with_not_perfect_division(self):
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=100,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user2, self.user3, self.user4)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 3)
        self.assertIn(
            {"payer": self.user2.id, "receiver": self.user1.id, "amount": "33.33"}, transactions
        )
        self.assertIn(
            {"payer": self.user3.id, "receiver": self.user1.id, "amount": "33.33"}, transactions
        )
        self.assertIn(
            {"payer": self.user4.id, "receiver": self.user1.id, "amount": "33.34"}, transactions
        )

    def test_get_minimum_settlements_with_multiple_expenses_and_multiple_debtors_and_creditors(
        self,
    ):
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=300,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user1, self.user2, self.user3)

        expense2 = Expense.objects.create(
            name="Expense 2",
            amount=200,
            group=self.group,
            paid_by=self.user2,
        )
        expense2.debtors.add(self.user1, self.user2, self.user3)

        expense3 = Expense.objects.create(
            name="Expense 3",
            amount=100,
            group=self.group,
            paid_by=self.user3,
        )
        expense3.debtors.add(self.user1, self.user2, self.user3)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 2)
        self.assertIn(
            {"payer": self.user3.id, "receiver": self.user1.id, "amount": "100.01"}, transactions
        )
        self.assertIn(
            {"payer": self.user3.id, "receiver": self.user2.id, "amount": "0.01"}, transactions
        )

    def test_with_single_expense_with_same_payer_and_debtor(self):
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=100,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user1)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 0)

    def test_with_single_expense_with_no_debtors(self):
        # Shouldn't be able to create an expense with no debtors but just in case
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=100,
            group=self.group,
            paid_by=self.user1,
        )

        expenses = Expense.objects.all()

        with self.assertRaises(ValueError) as context:
            _ = Expense.getMinimumSettlements(expenses)

        self.assertTrue(
            "Expense with id {} has no debtors".format(expense1.id) in str(context.exception)
        )

    def test_with_expense_with_amount_set_to_zero(self):
        # Shouldn't be able to create an expense with amount set to 0 but just in case
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=0,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user2)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 0)

    def test_with_expense_with_negative_amount(self):
        # Shouldn't be able to create an expense with amount set to a negative amount but in case
        expense1 = Expense.objects.create(
            name="Expense 1",
            amount=-100,
            group=self.group,
            paid_by=self.user1,
        )
        expense1.debtors.add(self.user2)

        expenses = Expense.objects.all()
        transactions = Expense.getMinimumSettlements(expenses)

        self.assertEqual(len(transactions), 1)
        self.assertIn(
            {"payer": self.user1.id, "receiver": self.user2.id, "amount": "100.00"}, transactions
        )
