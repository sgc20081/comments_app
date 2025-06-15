import graphene

from comments_service.schema import CommentType, CreateComment
from auth_service.schema import RegisterUser

class Query(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return CreateComment.objects.all()

class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    register_user = RegisterUser.field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)