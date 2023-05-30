from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from feed.accounts.serializers import RegisterSerializer, LoginSerializer, ConfirmCodeSerializer
from feed.accounts.models import ConfirmCode, User
from django.contrib.auth import authenticate
from random import choices

class RegistrationAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role')
        activate_code = ''.join(choices('0123456789', k=6))
        if role == 1:
            user = User.objects.create_superuser(username=username, password=password,
                                                 is_staff=True, role=role, is_superuser=True)
            return Response(status=status.HTTP_201_CREATED,
                            data={
                                'user_id': user.id,
                                "role": user.role
                            })
        else:
            user = User.objects.create_user(username=username, password=password, is_active=False, role=role)
            code = ConfirmCode.objects.create(user_id=user.id, code=activate_code)
            return Response(status=status.HTTP_201_CREATED,
                            data={
                                'user_id': user.id,
                                "role": user.role,
                                'code': code.code
                            })

class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if ConfirmCode.objects.filter(code=request.data['code']):
                User.objects.update(is_active=True)
                return Response(status=status.HTTP_202_ACCEPTED,
                                data={'success': 'confirmed'})

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'error': 'wrong id or code!'})

        except ValueError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'error': 'write code number!'})

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(data={
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'Username or password wrong!'})