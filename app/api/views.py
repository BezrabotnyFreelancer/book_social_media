from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    )
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE
from main.models import UserProfile, Book, Comment
from chat.models import Chat, Message
from .serializers import (
    UserProfileSerializer,
    BookSerializer,
    CommentSerializerForGETRequest,
    CommentSerializerForCreation,
    BookSerializerForUpdateOrNotAuthenticated,
    ChatSerializerForGETRequest,
    ChatSerializerForCreation,
    MessageSerializerForGETRequest,
    MessageSerializerForCreationUpdate
    )
from .permissions import IsOwnerOrReadOnly, IsOwnerOfMessage
from main.profile_methods import get_main_profile, get_profile, get_profile_by_id
from .return_objects import return_object_by_id
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
# Create your views here.


class UserPagesListAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


class UserProfileDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            for i in serializer.validated_data:
                if serializer.validated_data[i] == '' or serializer.validated_data is None:
                    instance.__setattr__(i, None)
                else:
                    instance.__setattr__(i, serializer.validated_data[i])
                instance.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'genre']

    def create(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_book = Book()
            for i in serializer.validated_data:
                new_book.__setattr__(i, serializer.validated_data[i])
            new_book.author = get_main_profile(self.request)
            new_book.file = self.request.FILES['file']
            if self.request.FILES.get('cover', False):
                new_book.cover = self.request.FILES['cover']
            new_book.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BookDetailUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.method == 'GET':
            return BookSerializer
        else:
            return BookSerializerForUpdateOrNotAuthenticated

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file
        cover = instance.cover
        serializer = BookSerializerForUpdateOrNotAuthenticated(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            for i in serializer.validated_data:
                instance.__setattr__(i, serializer.validated_data[i])
            instance.file = file
            if self.request.FILES.get('cover', False):
                instance.cover = self.request.FILES['cover']
            else:
                instance.cover = cover
            instance.author = get_main_profile(self.request)
            instance.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CommentListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        instance = return_object_by_id(self.kwargs.get('pk'), Book)
        queryset = Comment.objects.filter(book=instance)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializerForGETRequest
        else:
            return CommentSerializerForCreation

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializerForCreation(data=request.data)
        instance = return_object_by_id(self.kwargs.get('pk'), Book)
        if serializer.is_valid(raise_exception=True):
            new_comment = Comment()
            new_comment.author = get_main_profile(self.request)
            new_comment.book = instance
            new_comment.comment = serializer.validated_data['comment']
            new_comment.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ChatListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Chat.objects.filter(Q(user=get_main_profile(self.request)) | Q(recipient=get_main_profile(self.request)))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatSerializerForGETRequest
        else:
            return ChatSerializerForCreation

    def create(self, request, *args, **kwargs):
        serializer = ChatSerializerForCreation(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_chat = Chat()
            new_chat.user = get_main_profile(self.request)
            new_chat.recipient = get_profile(serializer.validated_data['recipient'])
            new_chat.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ChatMessagesListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        instance = return_object_by_id(self.kwargs.get('pk'), Chat)
        user_profile = get_main_profile(self.request)
        if user_profile != instance.recipient and user_profile != instance.user:
            raise PermissionDenied
        queryset = Message.objects.filter(chat=instance)
        unread_messages = Message.objects.filter(Q(chat=instance) | Q(is_read=False)).values('recipient_user')
        if unread_messages.count() > 0:
            recipient = unread_messages[0]['recipient_user']

            if user_profile == get_profile_by_id(recipient):
                queryset.update(is_read=True)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MessageSerializerForGETRequest
        else:
            return MessageSerializerForCreationUpdate

    def create(self, request, *args, **kwargs):
        instance = return_object_by_id(self.kwargs.get('pk'), Chat)
        serializer = MessageSerializerForCreationUpdate(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_message = Message()
            new_message.chat = instance
            new_message.sender_user = get_main_profile(self.request)
            if instance.recipient == get_main_profile(self.request):
                recipient = instance.user
            else:
                recipient = instance.recipient
            new_message.recipient_user = recipient
            new_message.body = serializer.validated_data['body']
            new_message.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MessageDetailUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOfMessage)
    serializer_class = MessageSerializerForCreationUpdate

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        chat = instance.chat
        recipient_user = instance.recipient_user
        sender_user = instance.sender_user
        date = instance.date
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance.chat = chat
            instance.recipient_user = recipient_user
            instance.sender_user = sender_user
            instance.body = serializer.validated_data['body']
            instance.date = date
            instance.is_edit = True
            instance.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
