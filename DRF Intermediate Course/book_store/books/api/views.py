from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.exceptions import ValidationError

from books.models import Book, Comment

from books.api.serializers import (
    BookSerializer,
    CommentSerializer,
)

from books.api.permissions import (
    IsAdminStaffOrReadOnly,
    IsCommentOwnerOrReadOnly
)

from books.api.pagination import SmallPagination


class BaseBook:
    queryset = Book.objects.order_by('id')
    serializer_class = BookSerializer
    pagination_class = SmallPagination
    permission_classes = [IsAdminStaffOrReadOnly]


class BaseComment:
    queryset = Comment.objects.order_by('id')
    serializer_class = CommentSerializer
    pagination_class = SmallPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookListCreateAPIView(BaseBook, ListCreateAPIView):
    pass


class BookDetailAPIView(BaseBook, RetrieveUpdateDestroyAPIView):
    pass


class CommentCreateAPIView(BaseComment, CreateAPIView):
    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_id')
        user_id = self.request.user.id

        already_commented = Comment.objects.filter(
            book=book_id, commentor_id=user_id).exists()
        if already_commented:
            raise ValidationError("You cannot comment more than once.")

        serializer.save(book_id=book_id, commentor_id=user_id)


class CommentListAPIView(BaseComment, ListAPIView):

    def get_queryset(self):
        return self.queryset.filter(commentor=self.request.user)


class CommentDetailAPIView(BaseComment, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentOwnerOrReadOnly]
