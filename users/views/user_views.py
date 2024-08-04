# ## docs openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from backend.shared.di.di import container
from backend.shared.views.base_view import (
    GenericAPIViewService,
)
from backend.shared.serializers.serializers import (
    BadRequestSerializer,
)
from backend.shared.constants.common_constants import page_size_openapi, page_openapi
from users.serializers.user_serializers import (
    UserCreateSerializer,
    UserFilterSerializer,
    UserOptDocWrapperSerializer,
    UserQueryDocWrapperSerializer,
)


class UserView(GenericAPIViewService):

    # constructor: DI
    def __init__(self):
        user_service = container.user_service()
        super().__init__(user_service)

    @swagger_auto_schema(
        operation_description="Get All Users",
        responses={
            200: openapi.Response("OK", UserQueryDocWrapperSerializer),
        },
        query_serializer=UserFilterSerializer,
        manual_parameters=[page_size_openapi, page_openapi],
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_description="Create User",
        request_body=UserCreateSerializer,
        responses={
            201: openapi.Response("OK", UserOptDocWrapperSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def post(self, request):
        return super().post(request)
