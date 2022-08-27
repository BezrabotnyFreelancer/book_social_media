from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import UserProfile, Book, Comment
# Register your models here.

class BookCommentInline(TabularInline):
    model = Comment
    

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['author', 'genre', 'title']
    list_filter = ['author']
    inlines = [BookCommentInline]


admin.site.register(UserProfile)
admin.site.register(Comment)
