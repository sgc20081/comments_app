from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({
                'username': [ErrorDetail("Wrong password or user does not exist")]
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                'username': [ErrorDetail("Wrong password or user does not exist")]
            })

        data = super().validate(attrs)
        return data