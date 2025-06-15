import graphene
from graphene_django.types import DjangoObjectType
from .models import Comment, CustomUser

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class CommentType(DjangoObjectType):
    author = graphene.Field(UserType)
    
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return Comment.objects.all()
    
class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, text, author_id):
        author = CustomUser.objects.get(id=author_id)
        comment = Comment.objects.create(text=text, author=author)
        return CreateComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)