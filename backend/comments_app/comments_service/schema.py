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

    def mutate(self, info, text):
        user = info.context.user

        comment = Comment.objects.create(text=text, author=user)
        return CreateComment(comment=comment)
    
class CommentsMutations(graphene.ObjectType):
    create_comment = CreateComment.Field()  