from django.shortcuts import render
from django.views.generic import ListView, DeleteView, FormView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
from .models import Chat
from main.profile_methods import get_main_profile, get_another_profile
from .forms import MessageSendForm


class ChatList(ListView):
    model = Chat
    context_object_name = 'chat_list'
    template_name = 'chat/chat_list.html'


def chat_detail_test(request):
    return HttpResponse(request, 'chat/chat_detail.html')


@login_required
def create_chat(request, pk):
    sender = get_main_profile(request)
    receiver = get_another_profile(pk)
    if request.method == 'POST':
        chat = Chat()
        chat.sender = sender
        chat.receiver = receiver
        chat.save()
        return HttpResponseRedirect(reverse('chat_detail'))
    else:
        return render(request, 'main/create_chat.html')
