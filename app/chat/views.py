from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# Create your views here.
from .forms import ChatForm, MessageForm
from .models import Chat, Message
from main.profile_methods import get_profile, get_main_profile, get_profile_by_id


@login_required
def create_chat(request):
    sender = get_main_profile(request)
    
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        
        if chat_form.is_valid():
            try:
                recipient = get_profile(chat_form.cleaned_data['username'])
            except:
                return render(request, 'chat/not_found_user.html')
            
            if sender == recipient:
                return redirect('create_chat')
            
            if Chat.objects.filter(user=get_main_profile(request), recipient=recipient).exists():
                chat = Chat.objects.get(user=get_main_profile(request), recipient=recipient)
                return redirect('chat', pk=chat.pk)
            
            elif Chat.objects.filter(user=recipient, recipient=get_main_profile(request)).exists():
                chat = Chat.objects.get(user=recipient, recipient=get_main_profile(request))
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

class MessageEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    fields = ('body',)
    model = Message
    template_name = 'chat/message_edit.html'
    
    def form_valid(self, form):
        message = form.save(commit=False)
        message.is_edit = True
        message.save()
        return super().form_valid(form) 
        
    def get_success_url(self):
        message = self.get_object()
        return message.chat.get_absolute_url()
    
    def test_func(self):
        message = self.get_object()
        return message.sender_user == get_main_profile(self.request)

class MessageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    login_url = reverse_lazy('account_login')
    template_name = 'chat/message_delete.html'
    
    def get_success_url(self):
        message = self.get_object()
        return message.chat.get_absolute_url()

    def test_func(self):
        message = self.get_object()
        return message.sender_user == get_main_profile(self.request)
    
@login_required
def chat_detail(request, pk):
    user_profile = get_main_profile(request)
    chat = Chat.objects.get(pk=pk)
    
    # Check of the chat profiles if other user get primary key
    if user_profile == chat.user or user_profile ==  chat.recipient: 
        message_list = Message.objects.filter(chat__pk__icontains=pk).order_by('date')
        unread_messages = Message.objects.filter(Q(chat__pk=pk) | Q(is_read=False)).values('recipient_user')
        if unread_messages.count() > 0:
            recipient = unread_messages[0]['recipient_user']
            
            if user_profile == get_profile_by_id(recipient):
                message_list.update(is_read=True)
        
        form = MessageForm()
        context = {
                'form': form,
                'chat': chat,
                'message_list': message_list,
                'user_profile': user_profile,
            }
        return render(request, 'chat/chat_detail.html', context=context)
    else:
        return redirect('inbox') 
