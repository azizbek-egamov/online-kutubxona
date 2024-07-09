from django.urls import path, re_path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('books/', KitoblarListCreateView.as_view(), name="books"),
    path('create-books/', kitoblarCreateView.as_view(), name="create-books"),
    path('delete-book/<int:pk>/', KitoblarDeleteView.as_view(), name="delete-book"),
    path('update-book/<int:pk>/', KitoblarUpdateView.as_view(), name="update-book"),
    path('books-api/<int:pk>/', BooksApi.as_view(), name="booksapi"),
    path('translate/', TranslatePage),
    path('wiki/', wikipediaPage),
    path('shortner/', UrlShortnerPage),
    path('book-view/', APIBooks.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 



