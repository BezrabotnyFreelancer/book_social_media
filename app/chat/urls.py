from django.urls import path
from . import views


urlpatterns = [
    path('inbox/', views.list_chats, name='inbox'),
    path('inbox/create-chat/', views.CreateChat.as_view(), name='create_chat'),
    path('inbox/<int:pk>/', views.ChatView.as_view(), name='chat'),
    path('inbox/<int:pk>/create-message/', views.CreateMessage.as_view(), name='create_message')
]