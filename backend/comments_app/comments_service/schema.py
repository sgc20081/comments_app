import graphene
from graphene_django.types import DjangoObjectType

from graphql_jwt.utils import jwt_encode
from graphql_jwt.settings import jwt_settings

from django.core.exceptions import ObjectDoesNotExist

from .models import Comment, CustomUser

def create_token(user):
    payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
    token = jwt_encode(payload)
    return token

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
    token = graphene.String()

    def mutate(self, info, text, author):
        request_user = info.context.user
        user = None
        token = None

        if request_user and request_user.is_authenticated:

            if request_user.username == author.username:
                user = request_user
            else:
                raise Exception("The user does not have permission to do this.")
        
        elif request_user and author.username:
            user = CustomUser.objects.filter(username=author.username).first()
            
            if not user:
                try:
                    user = CustomUser.objects.create(username=author.username, homepage=author.homepage)
                    token = create_token(user)
                    print(token)
                except Exception as e:
                    print(e.__class__.__name__, e, 'asdasd')
            else:
                raise Exception(f'Username: {author.username} is already taken')
        else:
            user = None

        comment = Comment.objects.create(text=text, author=user)
        return CreateCommentWithUser(comment=comment, token=token)


class Mutation(graphene.ObjectType):
    create_comment = CreateCommentWithUser.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)