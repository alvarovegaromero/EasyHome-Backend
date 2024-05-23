from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from groups.models import Group, UserGroup


class GroupGenerateCodeAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.group = Group.objects.create(
            name='Test Group',
            description='Test Description',
            currency='EUR',
            owner=self.user)
        self.url = f'/api/groups/{self.group.id}/generate_code'

    def test_generate_non_existent_group(self):
        response = self.client.get(f'/api/groups/9999/generate_code')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Group wasn't found")

    def test_generate_code_member(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('join_code' in response.data)

    def test_generate_code_non_member(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='otheruser@test.com',
            password='testpassword')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['error'],
            'You are not a member of this group.')
