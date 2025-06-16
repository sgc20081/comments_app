from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth import get_user_model

from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            content = super().create(request, *args, **kwargs)
        except Exception as e:
            print(f'Error: {self.__class__.__name__}: {e}')
            return Response({'errors': str(e)}, status=500)
        return Response({'success': True, 'status': 200, 'message': 'User registered successfully'})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            print(request.COOKIES)

            response = super().post(request, *args, **kwargs)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']

            access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            now = datetime.now()

            access_exp = now + access_lifetime
            refresh_exp = now + refresh_lifetime

            response.set_cookie(
                key='access_token',
                value=str(access),
                httponly=False,
                secure=True,
                samesite='None',
                max_age=access_lifetime,
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=False,
                secure=True,
                samesite='None',
                path='/auth/refresh/',
                max_age=refresh_lifetime,
            )
            
            response.data = {'access_exp': access_exp, 'refresh_exp': refresh_exp}

            return response
        except Exception as e:
            print(f'Error: {self.__class__.__name__}: {e}')
            errors = None
            # errors = errordetail_to_dict(e)
            # if not errors:
            #     errors = str(e)
            return Response({'errors': errors}, status=500)
        
        
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'No refresh token in cookies'}, status=401)

        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data['access']
            access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

            response.set_cookie(
                'access_token',
                access,
                max_age=access_lifetime,
                httponly=True,
                secure=True,
                samesite='None',
            )

            now = datetime.now()
            access_exp = now + access_lifetime
            response.data = {'access_exp': access_exp}
        return response