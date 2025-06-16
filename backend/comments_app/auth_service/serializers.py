import random
import string
import uuid
import hashlib

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

from .models import CustomUser

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')

        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError(
                [ErrorDetail("User with this username already exists")]
            )

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

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