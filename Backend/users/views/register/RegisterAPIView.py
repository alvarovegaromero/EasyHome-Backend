from rest_framework import status
from rest_framework.views import APIView
from venv import logger
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework.authtoken.models import Token


class RegisterAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            confirmation_password = request.data.get('confirmPassword')
            email = request.data.get('email')
            first_name = request.data.get('firstName', '')
            last_name = request.data.get('lastName', '')

            # Validations:
            if not username or not password or not confirmation_password or not email:
                return Response({'error': 'Username, password, confirmation password and email are required'}, status=status.HTTP_400_BAD_REQUEST)
            if password != confirmation_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
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
