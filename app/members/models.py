from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=16, unique=True, verbose_name='Username',
                                error_messages={"unique": _("A user with that username already exists.")})
    def __str__(self):
        return self.email



