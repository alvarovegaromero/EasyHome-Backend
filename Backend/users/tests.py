from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import LoginAPIView

class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.view = LoginAPIView.as_view()

    def test_login_success(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertTrue('token' in response.data)

    def test_login_no_username(self):
        request = self.factory.post('/login/', {'password': 'testpassword'})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
    
    def test_login_no_password(self):
        request = self.factory.post('/login/', {'username': 'testuser'})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
    
    def test_login_no_username_no_password(self):
        request = self.factory.post('/login/', {})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 401)   

    def test_login_non_existent_user(self):
        request = self.factory.post('/login/', {'username': 'nonexistentuser', 'password': 'testpassword'})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 401)