from django.urls import path
from . import views


urlpatterns = [
    path('chats/', views.ChatList.as_view(), name='chat_list'),
    path('chat_detail/', views.chat_detail_test, name='chat_detail'),
]