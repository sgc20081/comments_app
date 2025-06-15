from django.db import models

# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=15)

class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')

class ChildComment(Comment):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='child_comments')