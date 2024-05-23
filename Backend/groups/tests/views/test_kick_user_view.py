from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from groups.models import Group, UserGroup


class GroupKickUserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='testowner',
            email='testowner@test.com',
            password='testpassword')
        self.group = Group.objects.create(
            name='Test Group',
            description='Test Description',
            currency='EUR',
            owner=self.owner)
        self.token = Token.objects.create(user=self.owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.user_to_kick = User.objects.create_user(
            username='testuser2',
            email='testuser2@test.com',
            password='testpassword2')
        UserGroup.objects.create(user=self.user_to_kick, group=self.group)

    def test_kick_user(self):
        response = self.client.post(
            f'/api/groups/{self.group.id}/kick/{self.user_to_kick.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['success'],
            'User has been succesfully kicked from the group')

    def test_kick_user_nonexistent_group(self):
        response = self.client.post(
            f'/api/groups/9999/kick/{self.user_to_kick.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Group wasn't found")

    def test_kick_user_nonexistent_user(self):
        response = self.client.post(f'/api/groups/{self.group.id}/kick/9999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "User wasn't found")

    def test_kick_user_not_member(self):
        user_not_member = User.objects.create_user(
            username='testuser3',
            email='testuser3@test.com',
            password='testpassword3')
        response = self.client.post(
            f'/api/groups/{self.group.id}/kick/{user_not_member.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['error'],
            'User is not a member of this group')

    def test_kick_user_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' +
            Token.objects.create(
                user=self.user_to_kick).key)
        response = self.client.post(
            f'/api/groups/{self.group.id}/kick/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['error'],
            'Only the group owner can kick users')

    def test_kick_self(self):
        response = self.client.post(
            f'/api/groups/{self.group.id}/kick/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'You can not kick yourself. Leave the group instead')
