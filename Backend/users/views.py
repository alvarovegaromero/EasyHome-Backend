from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.validators import validate_email

class LoginAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'username': username}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials. Please, try again'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error("An error occurred during log in: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                # Delete the token when the user logout - Safer but costly. 
                # request.user.auth_token.delete() 
                logout(request)
                return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error("An error occurred during log out: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RegisterAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            first_name = request.data.get('firstName', '')
            last_name = request.data.get('lastName', '')

            # Validations:
            if not username or not password or not email:
                return Response({'error': 'Username, password, and email are required'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if password != request.data.get('confirmPassword'):
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                validate_email(email)
            except:
                return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Processing:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': username}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error("An error occurred during user registration: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileAPIView(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                return Response({'username': request.user.username, 'email': request.user.email, 'firstName': request.user.first_name, 'lastName': request.user.last_name}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error("An error occurred during profile retrieval: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            if request.user.is_authenticated:
                user = request.user
                username = request.data.get('username')
                email = request.data.get('email')
                first_name = request.data.get('firstName', '')
                last_name = request.data.get('lastName', '')

                if not username:
                    return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

                if not email:
                    return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

                if username != user.username:
                    if User.objects.filter(username=username).exists():
                        return Response({'error': 'Username already in use'}, status=status.HTTP_400_BAD_REQUEST)
                    user.username = username

                if email != user.email:
                    if User.objects.filter(email=email).exclude(username=user.username).exists():
                        return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    validate_email(email)
                except:
                    return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                return Response({'success': 'Profile updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error("An error occurred during profile update: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)