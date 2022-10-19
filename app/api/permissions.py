from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        try:
            user = obj.user
        except:
            user = obj.author.user

        return request.user == user


class IsOwnerOfMessage(BasePermission):
    def has_object_permission(self, request, view, obj):
        sender = obj.sender_user.user
        recipient = obj.recipient_user.user
        return request.user == sender or request.user == recipient
