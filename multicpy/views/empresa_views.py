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
from multicpy.serializers.empresa_serializers import (
    EmpresaSerializer,
    EmpresaQueryDocWrapperSerializer,
    EmpresaOptDocWrapperSerializer,
    EmpresaFilterSerializer,
)


class EmpresaView(GenericAPIViewService):

    # constructor: DI
    def __init__(self):
        empresa_service = container.empresa_service()
        super().__init__(empresa_service)

    @swagger_auto_schema(
        operation_description="Get All Empresas",
        responses={
            200: openapi.Response("OK", EmpresaQueryDocWrapperSerializer),
        },
        query_serializer=EmpresaFilterSerializer,
        manual_parameters=[page_size_openapi, page_openapi],
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_description="Create Empresa",
        request_body=EmpresaSerializer,
        responses={
            201: openapi.Response("OK", EmpresaOptDocWrapperSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def post(self, request):
        return super().post(request)


class EmpresaDetailView(BaseUpdateView):

    # constructor: DI
    def __init__(self):
        empresa_service = container.empresa_service()
        super().__init__(empresa_service)

    @swagger_auto_schema(
        operation_description="Update Empresa",
        request_body=EmpresaSerializer,
        responses={
            200: openapi.Response("OK", EmpresaOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
        },
    )
    def patch(self, request, pk):
        return super().patch(request, pk)

class EmpresaDetailViewByUuid(BaseRetrieveUuidView):
    # constructor: DI
    def __init__(self):
        empresa_service = container.empresa_service()
        super().__init__(empresa_service)

    @swagger_auto_schema(
        operation_description="Get Empresa by UUID",
        responses={
            200: openapi.Response("OK", EmpresaOptDocWrapperSerializer),
            404: openapi.Response("Not Found", NotFoundSerializer),
        },
    )
    def get(self, request, uuid):
        return super().get(request, uuid)
