from django.db import models

from auth_service.models import CustomUser

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='childs')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        parent = None
        
        if self.parent:
            parent = self.parent.text
        return (f'({self.__class__.__name__}: author = "{self.author.username}", text = "{self.text}", date = "{self.date_created}", parent = "{parent}")')
    
    def __repr__(self):
        parent = None

        if self.parent:
            parent = self.parent.text
        return (f'({self.__class__.__name__}: author = "{self.author.username}", text = "{self.text}", date = "{self.date_created}", parent = "{parent}")')