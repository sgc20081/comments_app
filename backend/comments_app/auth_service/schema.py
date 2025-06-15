import graphene

from graphql_jwt.utils import jwt_encode
from graphql_jwt.settings import jwt_settings

from django.core.exceptions import ObjectDoesNotExist

from .models import CustomUser

def create_token(user):
    payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
    token = jwt_encode(payload)
    return token

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username, password):
        if CustomUser.objects.filter(username=username).exists():
            return RegisterUser(success=False, message="Username already exists")

        user = CustomUser.objects.create_user(username=username, password=password)
        token = create_token(user)
        return RegisterUser(success=True, token=token, message="User registered")