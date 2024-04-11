from django.test import TestCase, RequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .views import LoginAPIView


class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.view = LoginAPIView.as_view()

    def test_login_success(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testusser')
        self.assertTrue('token' in response.data)