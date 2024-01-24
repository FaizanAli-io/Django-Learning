from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    publication_date = models.DateTimeField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.author}'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name="comments")

    commentor = models.CharField(max_length=255)
    comment = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.book} - {self.comment}'
