import strawberry
import strawberry_django

from strawberry import auto

from auth_service.types import CustomUserType

from .models import Comment

@strawberry_django.type(model=Comment)
class CommentType:
    id: auto
    text: auto
    author: "CustomUserType"
    date_created: auto
    parent: auto
    image: auto
    file: auto

@strawberry.type
class CreateCommentResponseType:
    success: bool
    status: int
    message: str | None = None
    comment: CommentType | None = None