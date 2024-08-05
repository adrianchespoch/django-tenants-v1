from django.urls import path

from books.views.book_views import (
    BookView,
    BookDetailView,
    BookDetailViewByUuid,
)


urlpatterns = [
    path('', BookView.as_view(), name='book'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('<str:uuid>/', BookDetailViewByUuid.as_view(), name='book-detail-uuid'),
]
