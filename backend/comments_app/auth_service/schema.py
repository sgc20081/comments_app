import graphene
from graphene_django.types import DjangoObjectType

from graphql_jwt.utils import jwt_encode
from graphql_jwt.settings import jwt_settings

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
        # print(success=True, user=user, token=token, message="User registered")
        return RegisterUser(success=True, user=user, token=token, message="User registered")
    
class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return LoginUser(success=False, message="Invalid credentials")

        token = create_token(user)
        return LoginUser(success=True, token=token, message="Login successful")

class AuthMutations(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()