from backend.shared.filters.filters import BaseFilter
from books.models.book_model import Book


class BookFilter(BaseFilter):
    class Meta:
        model = Book
        fields = '__all__'
