from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('search/books/', views.SearchResultBooks.as_view(), name='search_result_books'),
    path('search/authors/', views.SearchResultProfiles.as_view(), name='search_result_authors'),
    path('book/<uuid:pk>/', views.BookDetail.as_view(), name='book_detail'),
    path('<uuid:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile/', views.main_profile, name='main_profile'),
    path('edit/', views.main_profile_edit, name='main_profile_edit'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('create/book/', views.create_book, name='create_book')
]