from rest_framework import serializers

from backend.shared.serializers.serializers import (
    FiltersBaseSerializer,
    QueryDocWrapperSerializer,
    QueryListDocWrapperSerializer
)
from books.models.book_model import Book


# ### Book Serializer - Model ===============
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# ## Response: Get All & Get By ID
class BookResponseSerializer(FiltersBaseSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# ### Filter Serializer - Get All ===============
class BookFilterSerializer(FiltersBaseSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# ### Swagger ===============
# ## Response Body: Post & Put & Patch
class BookOptDocWrapperSerializer(QueryDocWrapperSerializer):
    data = BookResponseSerializer(required=False)


# ## Get All Response
class BookQueryDocWrapperSerializer(QueryListDocWrapperSerializer):
    data = BookResponseSerializer(many=True, required=False)
