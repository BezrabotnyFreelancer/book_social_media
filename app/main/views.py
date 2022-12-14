from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .profile_methods import get_main_profile
from django.db.models import Q
from django.views import View
# Create your views here.
from .models import UserProfile, Book
from .forms import UserProfileEdit, CreateBookForm, CommentForm
# Create your views here.


class HomePage(TemplateView):
    template_name = 'main/home.html'


class SearchResultBooks(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'main/book_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        books = Book.objects.filter(title__icontains=query)
        return books


class SearchResultProfiles(ListView):
    model = UserProfile
    context_object_name = 'profile_list'
    template_name = 'main/profile_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('a')
        return UserProfile.objects.filter(
            Q(user__username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )


class CommentBookGet(DetailView):
    model = Book
    template_name = 'main/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CommentBookPost(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Book
    form_class = CommentForm
    template_name = 'main/book_detail.html'
    login_url = reverse_lazy('account_login')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.book = self.object
        comment.author = get_main_profile(self.request)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        book = self.get_object()
        return reverse('book_detail', kwargs={'pk': book.pk})


class BookDetail(View):
    def get(self, request, *args, **kwargs):
        view = CommentBookGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentBookPost.as_view()
        return view(request, *args, **kwargs)


class BookDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    login_url = reverse_lazy('account_login')
    template_name = 'main/book_delete.html'
    success_url = reverse_lazy('main_profile')
    
    def test_func(self):
        book = self.get_object()
        return book.author == get_main_profile(self.request) 


class BookEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ('title', 'genre', 'subtitle', 'description', 'cover')
    login_url = reverse_lazy('account_login')
    template_name = 'main/book_edit.html'
    
    def get_success_url(self):
        book = self.get_object()
        return book.get_absolute_url()    
       
    def test_func(self):
        book = self.get_object()
        return book.author == get_main_profile(self.request)
    
    
class ProfileDetail(DetailView):
    model = UserProfile
    template_name = 'main/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        profile = self.get_object()
        books = Book.objects.filter(author=profile)
        context['books'] = books
        return context


class Settings(TemplateView):
    template_name = 'main/settings.html'


@login_required(login_url='account_login')
def create_book(request):
    profile = get_main_profile(request)
    if request.method == 'POST':
        book_form = CreateBookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = Book()
            book.author = profile
            for i in book_form.cleaned_data:
                book.__setattr__(i, book_form.cleaned_data[i])
            book.save()
            return redirect('book_detail', pk=book.pk)
        else:
            context = {'form': book_form}
            return render(request, 'main/create_book.html', context)
    else:
        book_form = CreateBookForm()
        context = {'form': book_form}
        return render(request, 'main/create_book.html', context)


@login_required(login_url='account_login')
def main_profile_edit(request):
    profile = get_main_profile(request)
    if request.method == 'POST':
        profile_form = UserProfileEdit(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('main_profile'))
        else:
            context = {'form': profile_form, 'profile': profile}
            return render(request, 'main/profile_edit.html', context)

    else:
        profile_form = UserProfileEdit(instance=profile)
        context = {'form': profile_form, 'profile': profile}
        return render(request, 'main/profile_edit.html', context)


@login_required(login_url='account_login')
def main_profile(request):
    profile = get_main_profile(request)
    books = Book.objects.filter(author=profile)
    return render(request, 'main/profile.html', {'profile': profile, 'books': books})
