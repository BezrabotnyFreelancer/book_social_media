from django.contrib import admin
from .models import UserProfile, Book, Comment
# Register your models here.


admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Comment)
