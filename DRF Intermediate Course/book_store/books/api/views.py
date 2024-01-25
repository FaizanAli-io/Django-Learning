from rest_framework.generics import (
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


class BaseBook:
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminStaffOrReadOnly]


class BaseComment:
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
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


class CommentDetailAPIView(BaseComment, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentOwnerOrReadOnly]
