from typing import Type

from backend.shared.services.base_service import BaseService

from books.models.book_model import Book
from books.filters.book_filters import BookFilter
from books.serializers.book_serializers import (
    BookSerializer,
    BookResponseSerializer,
)


class BookService(BaseService):
    model: Type[Book]

    filter = Type[BookFilter]

    serializer = Type[BookSerializer]
    serializer2 = Type[BookResponseSerializer]

    def __init__(self, model):
        filter = BookFilter
        serializer = BookSerializer
        serializer2 = BookResponseSerializer
        super().__init__(model, filter, serializer, serializer2)
