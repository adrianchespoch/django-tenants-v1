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
from users.serializers.extended_group_serializers import (
    ExtendedGroupSerializer,
    ExtendedGroupQueryDocWrapperSerializer,
    ExtendedGroupOptDocWrapperSerializer,
    ExtendedGroupFilterSerializer,
)


class ExtendedGroupView(GenericAPIViewService):

    # constructor: DI
    def __init__(self):
        extended_group_service = container.extended_group_service()
        super().__init__(extended_group_service)

    @swagger_auto_schema(
        operation_description="Get All ExtendedGroups",
        responses={
            200: openapi.Response("OK", ExtendedGroupQueryDocWrapperSerializer),
        },
        query_serializer=ExtendedGroupFilterSerializer,
        manual_parameters=[page_size_openapi, page_openapi],
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_description="Create ExtendedGroup",
        request_body=ExtendedGroupSerializer,
        responses={
            201: openapi.Response("OK", ExtendedGroupOptDocWrapperSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def post(self, request):
        return super().post(request)


class ExtendedGroupDetailView(BaseUpdateView):

    # constructor: DI
    def __init__(self):
        extended_group_service = container.extended_group_service()
        super().__init__(extended_group_service)

    @swagger_auto_schema(
        operation_description="Update ExtendedGroup",
        request_body=ExtendedGroupSerializer,
        responses={
            200: openapi.Response("OK", ExtendedGroupOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def patch(self, request, pk):
        return super().patch(request, pk)


class ExtendedGroupDetailViewByUuid(BaseRetrieveUuidView):
    # constructor: DI
    def __init__(self):
        extended_group_service = container.extended_group_service()
        super().__init__(extended_group_service)

    @swagger_auto_schema(
        operation_description="Get ExtendedGroup by UUID",
        responses={
            200: openapi.Response("OK", ExtendedGroupOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
        },
    )
    def get(self, request, uuid):
        return super().get(request, uuid)
