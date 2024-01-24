from rest_framework.generics import GenericAPIView

from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
)

from books.models import Book, Comment

from books.api.serializers import (
    BookSerializer,
    CommentSerializer,
)


class BookListCreateAPIView(CreateModelMixin, ListModelMixin, GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
