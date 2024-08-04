import os as osLib
from typing import Type
from rest_framework.authtoken.models import Token

from backend.shared.services.base_mixin_service import SerializationServiceMixin, PaginationServiceMixin
from backend.shared.exceptions.bad_request_exception import BadRequestException
from backend.shared.exceptions.resource_not_found_exception import ResourceNotFoundException
from backend.shared.exceptions.locked_request_exception import LockedRequestException
from backend.shared.exceptions.unauthorized_exception import UnauthorizedException
from backend.shared.exceptions.conflicts_exception import ConflictsException
from backend.shared.constants.common_constants import PAGINATION_DEFAULT_PAGE_NUMBER, PAGINATION_DEFAULT_PAGE_SIZE

from users.serializers.auth_serializers import (
    LoginSerializer,
    LoginResponseSerializer,
    PermissionSerializer,
)
from users.serializers.user_serializers import UserResponseSerializer
from users.shared.constants.system_modules import system_modules_sidenav

from users.models.user_model import User
from users.models.extended_group_model import ExtendedGroup
from django.contrib.auth.models import Group, Permission


# ### promote composition over inheritance
class AuthService(SerializationServiceMixin, PaginationServiceMixin):
    user_model: Type[User]
    group_model: Type[Group]
    permission_model: Type[Permission]
    extended_group_model: Type[ExtendedGroup]

    serializer = Type[LoginSerializer]
    serializer2 = Type[LoginResponseSerializer]
    user_serializer = Type[UserResponseSerializer]
    permission_serializer = Type[PermissionSerializer]

    # constructor: DI
    def __init__(self, group_model, permission_model, user_model, extended_group_model):
        self.group_model = group_model
        self.permission_model = permission_model
        self.user_model = user_model
        self.extended_group_model = extended_group_model
        self.serializer = LoginSerializer
        self.serializer2 = LoginResponseSerializer
        self.user_serializer = UserResponseSerializer
        self.permission_serializer = PermissionSerializer

    def login(self, data, ip: str | None = None, os: str | None = None) -> dict:
        user = self.user_model.objects.filter(
            username=data["username"]).first()
        if not user:
            raise BadRequestException("Credentials are invalid")

        failed_attempts = user.failed_login_attempts

        max_attempts = int(osLib.environ.get('MAX_FAILED_LOGIN_ATTEMPTS'))
        if failed_attempts >= max_attempts:
            raise LockedRequestException('User is locked')

        validated_login_data = self.validate_and_serialize(data=data)
        if not user.check_password(validated_login_data["password"]):
            user.failed_login_attempts += 1
            user.save()
            raise UnauthorizedException(
                message='Credentials are invalid',
                data={'failed_attempts': failed_attempts + 1}
            )

        force_login = validated_login_data.get('force_login', False)
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # Check if the user is trying to force login
            if force_login:
                token.delete()  # delete existing token
                token = Token.objects.create(user=user)  # create new token
            else:
                raise ConflictsException(message=f"Ya existe una sesión activa para este usuario en la dirección IP {user.ip_login}.", data={
                    "ip": user.ip_login,
                })

        user.failed_login_attempts = 0
        user.ip_login = ip
        user.save()

        user_permissions = user.get_all_permissions()
        user.permissions = sorted(user_permissions)

        # get system modules - group
        system_modules = []
        if user.is_superuser or user.is_staff:
            system_modules = system_modules_sidenav
        else:
            groups = user.groups.all()
            for group in groups:
                group_modules = self.extended_group_model.objects.filter(
                    group=group.id).values_list('module', flat=True)
                system_modules += group_modules

        return {
            'token': token.key,
            'user': self.user_serializer(user).data,
            'system_modules': list(set(system_modules)),
        }

    def find_permissions(self, user_id: int | None, group_id: int | None, page_number=PAGINATION_DEFAULT_PAGE_NUMBER, page_size=PAGINATION_DEFAULT_PAGE_SIZE) -> dict:
        # find permissions by user or group
        if user_id:
            return self.find_user_permissions(
                user_id, page_number, page_size)
        if group_id:
            return self.find_group_permissions(
                group_id, page_number, page_size)
        return self.find_all_permissions(page_number, page_size)

    def find_user_permissions(self, user_id: int, page_number=PAGINATION_DEFAULT_PAGE_NUMBER, page_size=PAGINATION_DEFAULT_PAGE_SIZE):
        user = self.user_model.objects.filter(user_id).first()
        if not user:
            raise ResourceNotFoundException(
                message=f'User with id {user_id} not found')

        user_permissions = user.user_permissions.all()
        group_permissions = self.permission_model.objects.filter(
            group__user=user).distinct()
        all_permissions = list(user_permissions) + list(group_permissions)
        queryset = list(set(all_permissions))
        return self._gen_paging_permissions_return(queryset, page_number, page_size)

    def find_group_permissions(self, group_id: int, page_number=PAGINATION_DEFAULT_PAGE_NUMBER, page_size=PAGINATION_DEFAULT_PAGE_SIZE):
        group = self.group_model.objects.filter(group_id).first()
        if not group:
            raise ResourceNotFoundException(
                message=f'Group with id {group_id} not found')

        queryset = group.permissions.all()
        return self._gen_paging_permissions_return(queryset, page_number, page_size)

    def find_all_permissions(self, page_number=PAGINATION_DEFAULT_PAGE_NUMBER, page_size=PAGINATION_DEFAULT_PAGE_SIZE):
        queryset = self.permission_model.objects.all()
        return self._gen_paging_permissions_return(queryset, page_number, page_size)

    def _gen_paging_permissions_return(self, queryset, page_number, page_size):
        paginated_data = self.paginate_queryset(
            queryset, page_number, page_size)
        serialized_data = self.permission_serializer(
            paginated_data['page_obj'], many=True
        ).data

        return {
            'meta': {
                'next': paginated_data['next_page'],
                'previous': paginated_data['previous_page'],
                'count': paginated_data['count'],
                'total_pages': paginated_data['total_pages'],
            },
            "data": serialized_data,
        }
