from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group, UserGroup


class UserGroupModelTest(TestCase):
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

    def test_is_member(self):
        user3 = User.objects.create_user(
            username="testuser3", email="testuser3@test.com", password="testpassword3"
        )

        self.assertTrue(UserGroup.is_member(self.user1, self.group))
        self.assertTrue(UserGroup.is_member(self.user2, self.group))
        self.assertFalse(UserGroup.is_member(user3, self.group))
