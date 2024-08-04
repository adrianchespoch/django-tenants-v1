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
from multicpy.serializers.suscripcion_serializers import (
    SuscripcionSerializer,
    SuscripcionQueryDocWrapperSerializer,
    SuscripcionOptDocWrapperSerializer,
    SuscripcionFilterSerializer,
)


class SuscripcionView(GenericAPIViewService):

    # constructor: DI
    def __init__(self):
        suscripcion_service = container.suscripcion_service()
        super().__init__(suscripcion_service)

    @swagger_auto_schema(
        operation_description="Get All Suscripcions",
        responses={
            200: openapi.Response("OK", SuscripcionQueryDocWrapperSerializer),
        },
        query_serializer=SuscripcionFilterSerializer,
        manual_parameters=[page_size_openapi, page_openapi],
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_description="Create Suscripcion",
        request_body=SuscripcionSerializer,
        responses={
            201: openapi.Response("OK", SuscripcionOptDocWrapperSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def post(self, request):
        return super().post(request)


class SuscripcionDetailView(BaseUpdateView):

    # constructor: DI
    def __init__(self):
        suscripcion_service = container.suscripcion_service()
        super().__init__(suscripcion_service)

    @swagger_auto_schema(
        operation_description="Update Suscripcion",
        request_body=SuscripcionSerializer,
        responses={
            200: openapi.Response("OK", SuscripcionOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def patch(self, request, pk):
        return super().patch(request, pk)

class SuscripcionDetailViewByUuid(BaseRetrieveUuidView):
    # constructor: DI
    def __init__(self):
        suscripcion_service = container.suscripcion_service()
        super().__init__(suscripcion_service)

    @swagger_auto_schema(
        operation_description="Get Suscripcion by UUID",
        responses={
            200: openapi.Response("OK", SuscripcionOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
        },
    )
    def get(self, request, uuid):
        return super().get(request, uuid)
