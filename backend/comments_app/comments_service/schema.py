import graphene
from graphene_django.types import DjangoObjectType

from auth_service.schema import UserType

from .models import Comment


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()
    status = graphene.Int()
    message = graphene.String()
    author = graphene.Field(UserType)

    def mutate(self, info, text):
        user = info.context.user
        print(user)
        if user and user.is_authenticated:
            print(user, user.is_authenticated)
            comment = Comment.objects.create(text=text, author=user)
            return CreateComment(success=True, status=200, comment=comment)
        else:
            return CreateComment(success=False, status=401, message='Only authorized users can writing comments')
    
class CommentsMutations(graphene.ObjectType):
    create_comment = CreateComment.Field()