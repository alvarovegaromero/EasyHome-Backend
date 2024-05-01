from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from groups.models import Group, UserGroup

class GroupsAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.group = Group.objects.create(name='Test Group', description='Test Description', currency='EUR', owner=self.user)
        self.url = '/api/groups/' 

    def test_get_groups(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['groups'][0]['id'], self.group.id)
        self.assertEqual(response.data['groups'][0]['name'], self.group.name)

    def test_get_groups_no_groups(self):
        UserGroup.objects.filter(user=self.user).delete() 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No groups found for this user.')