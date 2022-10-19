from rest_framework import serializers
from main.models import UserProfile, Book, Comment, user_directory_path
from chat.models import Chat, Message
from datetime import datetime


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=None)

    class Meta:
        model = Book
        fields = '__all__'


class BookSerializerForUpdateOrNotAuthenticated(serializers.ModelSerializer):
    author = serializers.HiddenField(default=None)
    file = serializers.HiddenField(default=None)

    class Meta:
        model = Book
        fields = '__all__'


class CommentSerializerForGETRequest(serializers.ModelSerializer):
    book = serializers.HiddenField(default=None)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializerForCreation(serializers.ModelSerializer):
    author = serializers.HiddenField(default=None)
    book = serializers.HiddenField(default=None)

    class Meta:
        model = Comment
        fields = '__all__'


class ChatSerializerForGETRequest(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatSerializerForCreation(serializers.ModelSerializer):
    user = serializers.HiddenField(default=None)
    recipient = serializers.CharField(max_length=16)

    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializerForGETRequest(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageSerializerForCreationUpdate(serializers.ModelSerializer):
    chat = serializers.HiddenField(default=None)
    sender_user = serializers.HiddenField(default=None)
    recipient_user = serializers.HiddenField(default=None)
    date = serializers.HiddenField(default=datetime.now())
    is_read = serializers.HiddenField(default=False)
    is_edit = serializers.HiddenField(default=False)

    class Meta:
        model = Message
        fields = '__all__'
