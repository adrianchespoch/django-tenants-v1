from typing import Type
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth.hashers import make_password  # hashear password

from backend.shared.services.base_service import BaseServiceAll
from backend.shared.exceptions.resource_not_found_exception import ResourceNotFoundException
from backend.shared.exceptions.bad_request_exception import BadRequestException

from users.serializers.user_serializers import UserCreateSerializer, UserResponseSerializer
from users.filters.user_filters import UserFilter
from users.models.user_model import User


class UserService(BaseServiceAll):
    model: Type[User]

    filter = Type[UserFilter]

    serializer = Type[UserCreateSerializer]
    serializer2 = Type[UserResponseSerializer]

    # DI: model
    def __init__(self, model):
        filter = UserFilter
        serializer = UserCreateSerializer
        serializer2 = UserResponseSerializer
        super().__init__(model, filter, serializer, serializer2)

    # @Override
    def create(self, data) -> dict:
        try:
            validated_data = self.validate_and_serialize(data)
            user_exists = self.model.objects.filter(
                username=validated_data['username']
            ).exists() or self.model.objects.filter(
                email=validated_data['email']
            ).exists()
            if user_exists:
                raise BadRequestException(
                    'El usuario o email ya ha sido registrado'
                )

            # work with transaction to automatically rollback if something goes wrong
            with transaction.atomic():
                saved_user = self.model.objects.create({
                    'username': validated_data['username'],
                    'email': validated_data['email'],
                    'password': make_password(validated_data['password']),
                    'razon_social': validated_data['razon_social'],
                    'groups': validated_data['groups'] if 'groups' in validated_data else []
                })

                return self.serializer2(saved_user).data

        except Exception as e:
            if isinstance(e, IntegrityError):
                raise ResourceNotFoundException(
                    message='Grupo no encontrado'
                )
            raise e

    # @Override
    def find_all(self, filter_params=None, page_number=..., page_size=...):
        from backend.shared.services.base_mixin_service import FindServiceMixin
        queryset = FindServiceMixin.find_all(self, self.filter, filter_params)
        paginated_data = self.paginate_queryset(
            queryset, page_number, page_size)
        serialized_data = self.serialize(paginated_data["page_obj"], many=True)
        paginated_profiles = {
            "meta": {
                "next": paginated_data["next_page"],
                "previous": paginated_data["previous_page"],
                "count": paginated_data["count"],
                "total_pages": paginated_data["total_pages"],
            },
            "data": serialized_data,
        }

        return {
            'meta': paginated_profiles['meta'],
            'data': paginated_profiles['data']
        }
