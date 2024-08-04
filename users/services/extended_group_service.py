from typing import Type

from backend.shared.services.base_service import BaseService
from backend.shared.exceptions.invalid_fields_exception import InvalidFieldsException
from backend.shared.exceptions.resource_not_found_exception import ResourceNotFoundException

from users.models.extended_group_model import ExtendedGroup
from users.filters.extended_group_filters import ExtendedGroupFilter
from users.serializers.extended_group_serializers import (
    ExtendedGroupSerializer,
    ExtendedGroupResponseSerializer,
)


class ExtendedGroupService(BaseService):
    model: Type[ExtendedGroup]

    filter = Type[ExtendedGroupFilter]

    serializer = Type[ExtendedGroupSerializer]
    serializer2 = Type[ExtendedGroupResponseSerializer]

    def __init__(self, model):
        filter = ExtendedGroupFilter
        serializer = ExtendedGroupSerializer
        serializer2 = ExtendedGroupResponseSerializer
        super().__init__(model, filter, serializer, serializer2)

    # @Override
    def create(self, data) -> dict:
        validated_data = self.validate_and_serialize(data)
        permissions = validated_data.pop("permissions", [])
        group = self.model.objects.create(**validated_data)
        if permissions:
            group.permissions.set(permissions)
        return self.serialize(group)

    def update(self, pk, data) -> dict:
        # use model 'cause of fin_one mixin method issues with pk
        group = self.model.objects.filter(pk=pk).first()
        if not group:
            raise ResourceNotFoundException(
                message=f"Resource with id '{pk}' not found"
            )
        serialied_group = self.serializer(
            instance=group, data=data, partial=True)
        if not serialied_group.is_valid():
            raise InvalidFieldsException(
                message="Bad Request", fields=serialied_group.errors.items()
            )
        permissions = serialied_group.validated_data.pop("permissions", None)
        for attr, value in serialied_group.validated_data.items():
            setattr(group, attr, value)
        group.save()
        if permissions is not None:
            group.permissions.set(permissions or [])
        return self.serialize(group)
