from django.test import TestCase
from django.contrib.auth.models import User
from groups.models import Group, UserGroup
import string
from django.utils import timezone

class GroupModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', email='testuser1@test.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', email='testuser2@test.com', password='testpassword2')
        self.group = Group.objects.create(name='Test Group', description='Test Description', currency='EUR', owner=self.user1)
        UserGroup.objects.create(user=self.user2, group=self.group)

    def test_generate_join_code(self):
        join_code = self.group.generate_join_code()
        self.assertEqual(len(join_code), 30)  
        self.assertTrue(all(c in string.ascii_letters + string.digits for c in join_code)) # Check that the join code only contains letters and digits
        self.assertEqual(self.group.join_code, join_code) 
        self.assertGreater(self.group.join_code_expiration, timezone.now())  # Check that the expiration date is in the future

        # Generate a new join code and check that it's different from the first one
        new_join_code = self.group.generate_join_code()
        self.assertNotEqual(join_code, new_join_code)

    def test_get_users(self):
        users = self.group.get_users()
        self.assertEqual(len(users), 2) 

        for user in users:
            if user['username'] == self.user1.username:
                self.assertEqual(user['id'], self.user1.id)
                self.assertTrue(user['is_owner'])
            elif user['username'] == self.user2.username:
                self.assertEqual(user['id'], self.user2.id)
                self.assertFalse(user['is_owner'])