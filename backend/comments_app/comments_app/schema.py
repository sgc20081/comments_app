# import graphene
import strawberry

from comments_service.schema import CommentsQuery, CommentsMutation

@strawberry.type
class Query(CommentsQuery):
    pass

@strawberry.type
class Mutation(CommentsMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)