import random

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'data': {
                'token': token.key,
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'is_verified': user.is_staff,
                    'is_superuser': user.is_superuser,
                }
            },
            'success': True,
            'errors': []
        }, status=200)


@api_view(['GET'])
@login_required(login_url='/users/login')
def is_verified_user(request):
    return Response({
        'data': {'message': 'User email verification status', 'is_verified': request.user.is_staff},
        'success': True,
        'errors': []
    })


@api_view(['GET'])
@login_required(login_url='/users/login')
def get_userdata(request):
    return Response({
        'data': {'user': {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username,
            'is_verified': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        }, },
        'success': True,
        'errors': []
    }, status=200)


class LoginView(APIView):

    def post(self, request):
        try:
            user = authenticate(username=request.data['username'], password=request.data['password'])
        except KeyError as e:
            return Response({
                'data': {},
                'success': False,
                'errors': ["You must specify 'username' and 'password'"]
            }, status=400)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'data': {
                    'token': token.key,
                    'user': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'username': user.username,
                        'is_verified': user.is_staff,
                        'is_superuser': user.is_superuser,
                    }
                },
                'success': True,
                'errors': []
            }, status=200)

        return Response({
            'data': {},
            'success': False,
            'errors': ['Invalid Credentials']
        }, status=400)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)

        return Response({
            'data': {'message': 'User Logged out successfully'},
            'success': True,
            'errors': []
        })


class VerifyEmail(APIView):
    """Sends a code to email for verification

    This is a Dummy view. No real verification is performed as of now.
    At the moment a code is printed to console using DjangoConsoleBackend.
    This view is written for practicing email verification.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        if request.user.is_staff:
            return Response({
                'data': {},
                'success': False,
                'errors': ['Email already verified']
            })

        else:
            send_mail(
                'Verification code',
                f'Your verification code is: {random.randint(1000, 9999)}',
                'cricinfo@django.com',
                [f'{request.user.email}'],
                fail_silently=False,
            )

            return Response({
                'data': {'message': 'Verification code is sent to your email address.'},
                'success': True,
                'errors': []
            })

    def post(self, request):
        try:
            code = request.data['verification_code']
        except KeyError as e:
            return Response({
                'data': {},
                'success': False,
                'errors': ["You must specify 'verification_code' sent to your email address."]
            })
        # Check if vrification code is correct
        request.user.is_staff = True
        request.user.save()
        return Response({
            'data': {'message': 'Verification Successfull.'},
            'success': True,
            'errors': []
        }, status=200)
