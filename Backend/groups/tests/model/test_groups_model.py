import string
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from expense_distribution.models import Expense
from groups.models import Group, UserGroup
from shared_board.models import SharedBoard


class GroupModelTest(TestCase):
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

        self.expense1 = Expense.objects.create(
            name="Expense 1",
            amount=100.20,
            paid_by=self.user1,
            group=self.group,
        )
        self.expense1.debtors.set([self.user1, self.user2])

        self.expense2 = Expense.objects.create(
            name="Expense 2",
            amount=200.05,
            paid_by=self.user2,
            group=self.group,
        )
        self.expense2.debtors.set([self.user1])

    def test_generate_join_code(self):
        join_code = self.group.generate_join_code()
        self.assertEqual(len(join_code), 30)
        # Check that the join code only contains letters and digits
        self.assertTrue(all(c in string.ascii_letters + string.digits for c in join_code))
        self.assertEqual(self.group.join_code, join_code)
        # Check that the expiration date is in the future
        self.assertGreater(self.group.join_code_expiration, timezone.now())

        # Generate a new join code and check that it's different from the first
        # one
        new_join_code = self.group.generate_join_code()
        self.assertNotEqual(join_code, new_join_code)

    def test_get_users(self):
        users = self.group.get_users()
        self.assertEqual(len(users), 2)

        for user in users:
            if user["username"] == self.user1.username:
                self.assertEqual(user["id"], self.user1.id)
                self.assertTrue(user["is_owner"])
            elif user["username"] == self.user2.username:
                self.assertEqual(user["id"], self.user2.id)
                self.assertFalse(user["is_owner"])

    def test_get_expenses(self):
        expenses = self.group.get_expenses()
        self.assertEqual(len(expenses), 2)

        for expense in expenses:
            if expense.id == self.expense1.id:
                self.assertEqual(expense.name, self.expense1.name)
                self.assertEqual(expense.amount, Decimal(str(self.expense1.amount)))
                self.assertEqual(expense.paid_by.username, self.user1.username)
                self.assertCountEqual(
                    [debtor.username for debtor in expense.debtors.all()],
                    [self.user1.username, self.user2.username],
                )
                self.assertEqual(expense.date_added, self.expense1.date_added)
                self.assertEqual(expense.date_paid, self.expense1.date_paid)
            elif expense.id == self.expense2.id:
                self.assertEqual(expense.name, self.expense2.name)
                self.assertEqual(expense.amount, Decimal(str(self.expense2.amount)))
                self.assertEqual(expense.paid_by.username, self.user2.username)
                self.assertCountEqual(
                    [debtor.username for debtor in expense.debtors.all()], [self.user1.username]
                )
                self.assertEqual(expense.date_added, self.expense2.date_added)
                self.assertEqual(expense.date_paid, self.expense2.date_paid)

    def test_group_creation_creates_sharedboard_and_usergroup(self):
        shared_board = SharedBoard.objects.filter(group=self.group)
        user_owner_group = UserGroup.objects.filter(group=self.group, user=self.user1)

        self.assertEqual(shared_board.exists(), True)
        self.assertEqual(user_owner_group.exists(), True)

    def test_group_delete_deletes_sharedboard_usergroup_and_expenses(self):
        group_id = self.group.id
        self.group.delete()
        shared_board = SharedBoard.objects.filter(group_id=group_id)
        user_owner_group = UserGroup.objects.filter(group_id=group_id, user=self.user1)

        expense1 = Expense.objects.filter(id=self.expense1.id)
        expense2 = Expense.objects.filter(id=self.expense2.id)

        self.assertEqual(shared_board.exists(), False)
        self.assertEqual(user_owner_group.exists(), False)
        self.assertEqual(expense1.exists(), False)
        self.assertEqual(expense2.exists(), False)
