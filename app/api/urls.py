from django.urls import path, include
from . import views


urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('profiles/', views.UserPagesListAPIView.as_view(), name='api-user_profiles'),
    path('profile/<uuid:pk>/', views.UserProfileDetailUpdateAPIView.as_view(), name='api-profile-detail-update'),
    path('books/', views.BookListCreateAPIView.as_view(), name='api-books'),
    path('book/<uuid:pk>/', views.BookDetailUpdateAPIView.as_view(), name='api-book-detail'),
    path('book/<uuid:pk>/comments/', views.CommentListCreateAPIView.as_view(), name='api-book-comments'),
    path('chats/', views.ChatListCreateAPIView.as_view(), name='api-chats'),
    path('chat/<uuid:pk>/', views.ChatMessagesListCreateAPIView.as_view(), name='api-chat-messages'),
    path('message/<uuid:pk>/', views.MessageDetailUpdateAPIView.as_view(), name='api-message-manage')
]
