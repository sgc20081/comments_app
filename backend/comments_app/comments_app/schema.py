import graphene

from comments_service.schema import CommentType, CreateComment

class Query(graphene.ObjectType):
    all_comments = graphene.List(CommentType)

    def resolve_all_comments(root, info):
        return CreateComment.objects.all()

class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)