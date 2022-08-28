from django.urls import path
from . import views


urlpatterns = [
    path('inbox/', views.list_chats, name='inbox'),
    path('inbox/create-chat/', views.create_chat, name='create_chat'),
    path('inbox/<uuid:pk>/', views.chat_detail, name='chat'),
    path('inbox/<uuid:pk>/create-message/', views.create_message, name='create_message'),
    path('inbox/<uuid:pk>/edit-message/', views.MessageEdit.as_view(), name='message_edit'),
    path('inbox/<uuid:pk>/delete-message/', views.MessageDelete.as_view(), name='message_delete')
]
