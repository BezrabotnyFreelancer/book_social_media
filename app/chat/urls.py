from django.urls import path
from . import views


urlpatterns = [
    path('inbox/', views.list_chats, name='inbox'),
    path('inbox/create-chat/', views.create_chat, name='create_chat'),
    path('inbox/<int:pk>/', views.chat_detail, name='chat'),
    path('inbox/<int:pk>/create-message/', views.create_message, name='create_message')
]