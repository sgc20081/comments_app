from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, homepage=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username, homepage=homepage)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, homepage=None):
        user = self.create_user(username, password, homepage)
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