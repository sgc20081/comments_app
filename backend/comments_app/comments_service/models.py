from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, homepage=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username, homepage=homepage)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, homepage=None):
        user = self.create_user(username, homepage)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    homepage = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

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