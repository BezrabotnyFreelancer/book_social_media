from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
# Register your models here.
from .models import Message, Chat

class ChatMessageInline(TabularInline):
    model = Message
    extra = 0
    
class ChatModelAdmin(ModelAdmin):
    inlines = [ChatMessageInline]
    list_filter = ['user']
    
admin.site.register(Chat, ChatModelAdmin)