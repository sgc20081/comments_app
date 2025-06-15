import graphene

from comments_service.schema import CommentType, CreateComment, CommentsMutations
from auth_service.schema import AuthMutations

class Query(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return CreateComment.objects.all()

class Mutation(AuthMutations, CommentsMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)