import graphene
from graphene_django.types import DjangoObjectType

import graphql_jwt

from django.core.exceptions import ObjectDoesNotExist

from .models import Comment, CustomUser

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return Comment.objects.all()

class UserInput(graphene.InputObjectType):
    username = graphene.String()
    homepage = graphene.String()

class CreateCommentWithUser(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)
        author = graphene.Argument(UserInput)

    comment = graphene.Field(CommentType)

    def mutate(self, info, text, author):
        user = None
        try:
            user = CustomUser.objects.get(username=author.username)
            print(user)
        except ObjectDoesNotExist as e:
            print(e)
            try:
                user = CustomUser.objects.create(username=author.username, homepage=author.homepage)
            except Exception as e2:
                print(e2.__class__.__name__, e2)

        comment = Comment.objects.create(text=text, author=user)
        return CreateCommentWithUser(comment=comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateCommentWithUser.Field()

class ObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        print()
        return cls(user=info.context.user)
    

schema = graphene.Schema(query=Query, mutation=Mutation)