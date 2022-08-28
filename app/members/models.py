from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=16, unique=True, verbose_name='Username',
                                error_messages={"unique": _("A user with that username already exists.")})
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'        
        
    def __str__(self):
        return self.email



