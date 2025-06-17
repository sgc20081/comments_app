from graphene_django.types import DjangoObjectType

from .models import CustomUser

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "homepage")