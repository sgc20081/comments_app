from django.shortcuts import render

from .models import CustomUser, Comment
# Create your views here.

def test(request, *args, **kwargs):
    test_user = CustomUser.objects.create(username='test')
    test_comment = Comment.objects.create(author=test_user, text='TEST TEXT FOR COMMENT')
    test_comment_2 = Comment.objects.create(author=test_user, text='TEST TEXT FOR child COMMENT', parent=test_comment)

    print(test_comment)
    print(test_comment_2)