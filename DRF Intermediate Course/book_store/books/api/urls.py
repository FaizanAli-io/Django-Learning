from django.urls import path

from books.api.views import (
    BookListCreateAPIView,
    BookDetailAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
)

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list'),
    path('books/<int:pk>', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:book_id>/addcomment', CommentCreateAPIView.as_view(),
         name='comment-add'),

    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>', CommentDetailAPIView.as_view(),
         name='comment-detail'),
]
