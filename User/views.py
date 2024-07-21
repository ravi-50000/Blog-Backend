import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.serializers import RegisterRequestSerializer, LoginRequestSerializer, LogoutRequestSerializer
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
logger = logging.getLogger(settings.DEBUG_LOGGER_DJANGO)

class Register(APIView):
    """
    Register a new user.

    POST /register/
    Request Body:
    - username
    - password
    - email

    Response:
    - Message: 'Registered Successfully'
    """
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('User registered successfully.')
            return Response({'Message': 'Registered Successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception('Error during registration: %s', str(e))
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):
    """
    Log in and get JWT tokens.

    POST /signin/
    Request Body:
    - username
    - password

    Response:
    - access: Access token
    - refresh: Refresh token
    """
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            if User.objects.filter(username=username).exists():
                logger.warning('Incorrect password for user: %s', username)
                return Response({'Error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.warning('User does not exist: %s', username)
                return Response({'Error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            logger.info('User %s logged in successfully.', username)
            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            logger.exception('Token error during login: %s', str(e))
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception('Unexpected error during login: %s', str(e))
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogOut(APIView):
    """
    Log out by blacklisting the refresh token.

    POST /logout/
    Request Body:
    - refresh_token

    Response:
    - message: 'Logged out successfully'
    """
    permission_classes = [IsAuthenticated]
     
    def post(self, request):
        try:
            request_serializer = LogoutRequestSerializer(data=request.data)
            if request_serializer.is_valid(raise_exception=True):
                refresh_token = request_serializer.validated_data['refresh_token']
                
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info('Refresh token blacklisted successfully.')
            except TokenError as e:
                logger.exception('Token error during logout: %s', str(e))
                return Response({'Refresh token Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Unexpected error during logout: %s', str(e))
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
