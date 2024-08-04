from typing import Type
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# ## docs openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ### Authentication & Authorization
from rest_framework.authentication import TokenAuthentication  # permissions
from rest_framework.permissions import IsAuthenticated  # authentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.shared.di.di import container
from backend.shared.mixins.common_mixin import AuthAdminViewMixin
from backend.shared.utils.handle_rest_exception_helper import handle_rest_exception_helper
from backend.shared.utils.pagination_utils import get_pagination_parameters_rest
from backend.shared.serializers.serializers import (
    BadRequestSerializer,
)

from backend.shared.constants.common_constants import page_size_openapi, page_openapi
from users.serializers.auth_serializers import (
    LoginSerializer,
)
from users.services.auth_service import AuthService
from users.serializers.auth_serializers import LoginResponseDocWrapperSerializer, PermissionListQueryDocWrapperSerializer


class LoginCustomView(APIView):
    service = Type[AuthService]

    # constructor: DI
    def __init__(self):
        self.service = container.auth_service()

    @swagger_auto_schema(
        operation_description="User Login",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("OK", LoginResponseDocWrapperSerializer),
            400: openapi.Response("Bad Request", BadRequestSerializer),
            401: openapi.Response(
                "Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            "failed_attempts": openapi.Schema(type=openapi.TYPE_INTEGER, description="Failed login attempts"),
                        }),
                    },
                )
            ),
            409: openapi.Response(
                "Session already exists for this user.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            "ip": openapi.Schema(type=openapi.TYPE_STRING),
                            "os": openapi.Schema(type=openapi.TYPE_STRING),
                        }),
                    },
                )
            ),
        },
    )
    def post(self, request):
        try:
            ip = request.META.get('REMOTE_ADDR') if request.META.get(
                'REMOTE_ADDR') else request.META.get('HTTP_X_FORWARDED_FOR')
            os = request.META.get('HTTP_USER_AGENT') if request.META.get(
                'HTTP_USER_AGENT') else None

            serialized_data = self.service.login(
                data=request.data, ip=ip, os=os)

            return Response({
                "status": status.HTTP_200_OK,
                "message": "Inicio de sesión exitoso",
                "data": serialized_data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_rest_exception_helper(e)


# ### Logout in this way 'case avoid class-based issues with auth and permissions in logout
# auth and permissions

@swagger_auto_schema(
    method="post",
    operation_description="User Logout",
    responses={
        200: openapi.Response("OK", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_INTEGER),
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ))
    },
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Sesión cerrada exitosamente.",
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            "status": "error",
            "message": "Ocurrió un error al cerrar la sesión.",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ### Authorization ============================
class PermissionsCustomView(AuthAdminViewMixin):
    auth_service = Type[AuthService]

    # constructor: DI
    def __init__(self):
        self.auth_service = container.auth_service()

    @swagger_auto_schema(
        operation_description="Get permission list",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID to get permissions", type=openapi.TYPE_INTEGER),
            openapi.Parameter('group_id', openapi.IN_QUERY,
                              description="Group ID to get permissions", type=openapi.TYPE_INTEGER),
            page_openapi,
            page_size_openapi,
        ],
        responses={
            200: openapi.Response("OK", PermissionListQueryDocWrapperSerializer),
            401: openapi.Response("Unauthorized", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                },
            )),
        },
    )
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id', None)
            group_id = request.query_params.get('group_id', None)
            _, page_number, page_size = get_pagination_parameters_rest(request)

            serialized_data = self.auth_service.find_permissions(
                user_id=user_id, group_id=group_id, page_number=page_number, page_size=page_size)

            return Response({
                "status": status.HTTP_200_OK,
                "message": "Lista de permisos obtenida",
                "data": serialized_data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_rest_exception_helper(e)


class GroupPermissionsCustomView(AuthAdminViewMixin):
    auth_service = Type[AuthService]

    # constructor: DI
    def __init__(self):
        self.auth_service = container.auth_service()

    @swagger_auto_schema(
        operation_description="Get permission list by Group ID",
        manual_parameters=[
            page_openapi,
            page_size_openapi,
            openapi.Parameter('group_id', openapi.IN_PATH,
                              description="Group ID to get permissions",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response("OK", PermissionListQueryDocWrapperSerializer),
            401: openapi.Response("Unauthorized", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                },
            )),
        },
    )
    def get(self, request, group_id):
        try:
            _, page_number, page_size = get_pagination_parameters_rest(request)
            serialized_data = self.auth_service.find_group_permissions(
                group_id=group_id, page_number=page_number, page_size=page_size)

            return Response({
                "status": status.HTTP_200_OK,
                "message": "Lista de permisos obtenida",
                "data": serialized_data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_rest_exception_helper(e)
