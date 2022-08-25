from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import ChatForm, MessageForm
from .models import Chat, Message
from main.profile_methods import get_profile, get_main_profile


class CreateChat(LoginRequiredMixin, View):
    
    login_url = reverse_lazy('login')
    
    def get(self, request, *args, **kwargs):
        form = ChatForm()
        context = {
            'form': form
        }
        
        return render(request, 'chat/create_chat.html', context=context)
    
    def post(self, request, *args, **kwargs):
        form = ChatForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
        
            try:
                recipient = get_profile(username)
                
                if Chat.objects.filter(user=request.user, recepient=recipient).exists():
                    chat = Chat.objects.filter(user=get_main_profile(request), recipient=recipient)[0]
                    return redirect('chat', pk=chat.pk)
                
                if form.is_valid():
                    sender_chat = Chat(
                        user=get_main_profile(request),
                        recipient=recipient
                    )
                    sender_chat.save()
                    chat_pk = sender_chat.pk
                    return redirect('chat', pk=chat_pk)
            except:
                return redirect('create_chat')


@login_required
def list_chats(request):
    chats = Chat.objects.filter(Q(user=get_main_profile(request)) | Q(recipient=get_main_profile(request)))
        
    
    context = {
        'chats': chats
    }
    
    return render(request, 'chat/inbox.html', context)


class CreateMessage(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    
    def post(self, request, pk, *args, **kwargs):
        chat = Chat.objects.get(pk=pk)
        
        if chat.recipient == get_main_profile(request):
            recipient = chat.user
            
        else:
            recipient = chat.recipient
            message_form = MessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                message = Message()
                message.chat = chat
                message.sender_user = get_main_profile(request)
                message.recipient_user = recipient
                message.body = message_form.cleaned_data['body']
                message.files = message_form.cleaned_data['files']
                message.save()
            
            return redirect('chat', pk=pk)


class ChatView(LoginRequiredMixin, View):
    
    login_url = reverse_lazy('login')
    
    def get(self, request, pk, *args, **kwargs):
        
        form = MessageForm()
        chat = Chat.objects.get(pk=pk)
        message_list = Message.objects.filter(chat__pk__icontains=pk)
        user = get_main_profile(request)
        
        context = {
            'form': form,
            'chat': chat,
            'message_list': message_list,
            'user': user
        }
        
        return render(request, 'chat/chat_detail.html', context=context)
    
    