import strawberry_django
from strawberry import auto

# from comments_service.types import CommentType

from .models import CustomUser

@strawberry_django.type(model=CustomUser)
class CustomUserType:
    id: auto
    username: auto
    homepage: auto
    # comments: list[CommentType]