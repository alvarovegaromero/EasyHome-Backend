from django.test import TestCase
from django.contrib.auth.models import User
from groups.models import Group
import string
from django.utils import timezone

class GroupModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.group = Group.objects.create(name='Test Group', description='Test Description', currency='EUR', owner=self.user)

    def test_generate_join_code(self):
        join_code = self.group.generate_join_code()
        self.assertEqual(len(join_code), 30)  # Check that the join code has the correct length
        self.assertTrue(all(c in string.ascii_letters + string.digits for c in join_code))  # Check that the join code only contains letters and digits
        self.assertEqual(self.group.join_code, join_code)  # Check that the join code was saved to the group
        self.assertGreater(self.group.join_code_expiration, timezone.now())  # Check that the expiration date is in the future

        # Generate a new join code and check that it's different from the first one
        new_join_code = self.group.generate_join_code()
        self.assertNotEqual(join_code, new_join_code)