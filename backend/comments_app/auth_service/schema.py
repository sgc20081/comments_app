import graphene
from graphene_django.types import DjangoObjectType

from graphql_jwt.utils import jwt_encode, jwt_payload
from graphql_jwt.refresh_token.models import RefreshToken
from graphql_jwt.shortcuts import get_refresh_token
from graphql_jwt.settings import jwt_settings

from graphql_jwt.decorators import exceptions

from django.contrib.auth import authenticate

from .models import CustomUser

def create_token(user):
    payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
    token = jwt_encode(payload)
    return token

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "homepage")