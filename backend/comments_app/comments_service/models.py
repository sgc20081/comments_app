from django.db import models

# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=15)
    homepage = models.URLField(blank=True)

    def __str__(self):
        return (f'({self.__class__.__name__}: username = "{self.username}", homepage = "{self.homepage}")')
    
    def __repr__(self):
        return (f'({self.__class__.__name__}: username = "{self.username}", homepage = "{self.homepage}")')

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