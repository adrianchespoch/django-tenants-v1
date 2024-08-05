# ## docs openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from backend.shared.di.di import container
from backend.shared.views.base_view import (
    GenericAPIViewService,
    BaseUpdateView,
    BaseRetrieveUuidView,
)
from backend.shared.serializers.serializers import (
    BadRequestSerializer,
    NotFoundSerializer,
)

from backend.shared.constants.common_constants import page_size_openapi, page_openapi
from books.serializers.book_serializers import (
    BookSerializer,
    BookQueryDocWrapperSerializer,
    BookOptDocWrapperSerializer,
    BookFilterSerializer,
)


class BookView(GenericAPIViewService):

    # constructor: DI
    def __init__(self):
        book_service = container.book_service()
        super().__init__(book_service)

    @swagger_auto_schema(
        operation_description="Get All Books",
        responses={
            200: openapi.Response("OK", BookQueryDocWrapperSerializer),
        },
        query_serializer=BookFilterSerializer,
        manual_parameters=[page_size_openapi, page_openapi],
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_description="Create Book",
        request_body=BookSerializer,
        responses={
            201: openapi.Response("OK", BookOptDocWrapperSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def post(self, request):
        return super().post(request)


class BookDetailView(BaseUpdateView):

    # constructor: DI
    def __init__(self):
        book_service = container.book_service()
        super().__init__(book_service)

    @swagger_auto_schema(
        operation_description="Update Book",
        request_body=BookSerializer,
        responses={
            200: openapi.Response("OK", BookOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def patch(self, request, pk):
        return super().patch(request, pk)

class BookDetailViewByUuid(BaseRetrieveUuidView):
    # constructor: DI
    def __init__(self):
        book_service = container.book_service()
        super().__init__(book_service)

    @swagger_auto_schema(
        operation_description="Get Book by UUID",
        responses={
            200: openapi.Response("OK", BookOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
        },
    )
    def get(self, request, uuid):
        return super().get(request, uuid)
