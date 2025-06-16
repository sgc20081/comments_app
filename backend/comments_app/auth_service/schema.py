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

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username, password):
        if CustomUser.objects.filter(username=username).exists():
            return RegisterUser(success=False, message="Username already exists")

        user = CustomUser.objects.create_user(username=username, password=password)
        token = create_token(user)
        return RegisterUser(success=True, user=user, token=token, message="User registered")
    
class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    # token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()
    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return LoginUser(success=False, message="Invalid credentials")
        
        payload = jwt_payload(user)
        access_token = jwt_encode(payload)
        refresh_token = None

        try:
            refresh_token = get_refresh_token(user)
        except exceptions.JSONWebTokenError as e:
            refresh_token_obj = RefreshToken.objects.create(user=user)
            print(refresh_token_obj.__dict__)
            refresh_token = str(refresh_token_obj.token)
        
        print(f'JWT Refresh: {refresh_token}')

        # Установка в куки
        # response = info.context
        # response.set_cookie(
        #     'access_token',
        #     access_token,
        #     httponly=True,
        #     samesite='Lax',
        #     max_age=300,
        #     secure=False,  # True для HTTPS
        #     path='/graphql/',
        # )
        # response.set_cookie(
        #     'refresh_token',
        #     refresh_token,
        #     httponly=True,
        #     samesite='Lax',
        #     max_age=60 * 60 * 24 * 7,
        #     secure=False,
        #     path='/graphql/',
        # )


        # token = create_token(user)
        return LoginUser(
            success=True, 
            user=user, 
            message="Login successful",
            access_token=access_token,
            refresh_token=refresh_token
        )

class AuthMutations(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()