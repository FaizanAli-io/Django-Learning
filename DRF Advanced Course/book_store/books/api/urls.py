from django.urls import path

from books.api.views import BookListCreateAPIView

urlpatterns = [
    path('books', BookListCreateAPIView.as_view(), name='book-list'),
]
