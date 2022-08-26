from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import ChatForm, MessageForm
from .models import Chat, Message
from main.profile_methods import get_profile, get_main_profile


@login_required
def create_chat(request):
    sender = get_main_profile(request)
    
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        
        if chat_form.is_valid():
            recipient = get_profile(chat_form.cleaned_data['username'])
            
            if Chat.objects.filter(user=get_main_profile(request), recipient=recipient).exists():
                chat = Chat.objects.get(user=get_main_profile(request), recipient=recipient)
                return redirect('chat', pk=chat.pk)
            
            else:
                chat = Chat()
                chat.user = sender
                chat.recipient = recipient
                chat.save()
                return redirect('chat', pk=chat.pk)
            
        else:
            context = {'form': chat_form}
            return render(request, 'chat/create_chat.html', context)
    
    else:
        chat_form = ChatForm()
        context = {'form': chat_form}
        return render(request, 'chat/create_chat.html', context)
    

@login_required
def list_chats(request):
    chats = Chat.objects.filter(Q(user=get_main_profile(request)) | Q(recipient=get_main_profile(request)))
        
    
    context = {
        'chats': chats
    }
    
    return render(request, 'chat/inbox.html', context)

@login_required
def create_message(request, pk):
    chat = Chat.objects.get(pk=pk)
    
    if chat.recipient == get_main_profile(request):
        recipient = chat.user
        
    else:
        recipient = chat.recipient
        
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        
        if message_form.is_valid():
            message = Message()
            message.chat = chat
            message.sender_user = get_main_profile(request)
            message.recipient_user = recipient
            message.body = message_form.cleaned_data['body']
            message.save()
            return HttpResponseRedirect(reverse('chat', kwargs={'pk': pk}))
        
        else:
            context = {'form': message_form}
            return render(request, 'chat/chat_detail.html', context)
        
    else:
        message_form = MessageForm()
        context = {'form': message_form}
        return render(request, 'chat/chat_detail.html', context)
            
        
@login_required
def chat_detail(request, pk):
    user = get_main_profile(request)
    chat = Chat.objects.get(pk=pk)
    message_list = Message.objects.filter(chat__pk__icontains=pk)
    form = MessageForm()
    context = {
            'form': form,
            'chat': chat,
            'message_list': message_list,
            'user': user,
        }
    return render(request, 'chat/chat_detail.html', context=context) 