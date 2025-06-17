# import graphene
# from graphene_django.types import DjangoObjectType

# from auth_service.schema import UserType

# import strawberry
# from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL
# from typing import AsyncGenerator

# from .models import Comment


# class CommentType(DjangoObjectType):
#     class Meta:
#         model = Comment

# class CreateComment(graphene.Mutation):
#     class Arguments:
#         text = graphene.String(required=True)

#     comment = graphene.Field(CommentType)
#     success = graphene.Boolean()
#     status = graphene.Int()
#     message = graphene.String()
#     author = graphene.Field(UserType)

#     def mutate(self, info, text):
#         user = info.context.user
#         print(repr(user))
#         if user and user.is_authenticated:
#             print(user, user.is_authenticated)
#             comment = Comment.objects.create(text=text, author=user)
#             return CreateComment(success=True, status=200, comment=comment)
#         else:
#             return CreateComment(success=False, status=401, message='Only authorized users can writing comments')

# class CommentsQuery(graphene.ObjectType):
#     all_comments = graphene.List(CommentType)

#     def resolve_all_comments(root, info):
#         return Comment.objects.all()

# class CommentsMutations(graphene.ObjectType):
#     create_comment = CreateComment.Field()

# schema.py
import asyncio
import strawberry

from typing import AsyncGenerator

from .types import CommentType, CreateCommentResponseType
from .models import Comment

# @strawberry_type(Comment)
# class CommentType:
#     pass

@strawberry.type
class CommentsMutation:
    @strawberry.mutation
    def create_comment(self, text: str, info) -> CreateCommentResponseType:
        user = info.context.request.user
        print(info.context.request.__dict__)
        print(user)
        if user and user.is_authenticated:
            print(user, user.is_authenticated)
            comment = Comment.objects.create(text=text, author=user)
            return CreateCommentResponseType(success=True, status=200, comment=comment)
        else:
            return CreateCommentResponseType(success=False, status=401, message='Only authorized users can writing comments')
        
        if not user.is_authenticated:
            raise Exception("Unauthorized")
        comment = Comment.objects.create(text=text, author=user)
        # Пушим в глобальную очередь для подписки
        COMMENT_QUEUE.put_nowait(comment)
        return comment

COMMENT_QUEUE = asyncio.Queue()

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def comment_stream(self) -> AsyncGenerator[CommentType, None]:
        while True:
            comment = await COMMENT_QUEUE.get()
            yield comment

@strawberry.type
class CommentsQuery:
    @strawberry.field
    def all_comments(self) -> list[CommentType]:
        return Comment.objects.all()

# schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
