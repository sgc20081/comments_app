import graphene
from graphene_django.types import DjangoObjectType

from .models import Comment

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, text):
        user = info.context.user

        if user and user.is_authenticated:
            comment = Comment.objects.create(text=text, author=user)
            return CreateComment(comment=comment)
        else:
            return CreateComment(success=False, message='Only authorized users can writing comments')
    
class CommentsMutations(graphene.ObjectType):
    create_comment = CreateComment.Field()  