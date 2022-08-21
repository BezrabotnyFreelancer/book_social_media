from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return Book.objects.filter(title__icontains=query)


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
        comment.author = get_profile(self.request)
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


class ProfileDetail(DetailView):
    model = UserProfile
    template_name = 'main/profile.html'
    context_object_name = 'profile'


class Settings(TemplateView):
    template_name = 'main/settings.html'


@login_required
def create_book(request):
    profile = get_main_profile(request)
    if request.method == 'POST':
        book_form = CreateBookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = Book()
            book.author = profile
            book.title = book_form.cleaned_data['title']
            book.genre = book_form.cleaned_data['genre']
            book.subtitle = book_form.cleaned_data['subtitle']
            book.description = book_form.cleaned_data['description']
            book.file = book_form.cleaned_data['file']
            book.cover = book_form.cleaned_data['cover']
            book.save()
            profile.book.add(book)
            profile.save()
            return HttpResponseRedirect(reverse('main_profile'))
        else:
            context = {'form': book_form}
            return render(request, 'main/create_book.html', context)
    else:
        book_form = CreateBookForm()
        context = {'form': book_form}
        return render(request, 'main/create_book.html', context)


@login_required
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


@login_required
def main_profile(request):
    profile = get_main_profile(request)
    return render(request, 'main/profile.html', {'profile': profile})