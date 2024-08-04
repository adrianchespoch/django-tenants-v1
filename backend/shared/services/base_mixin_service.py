from backend.shared.exceptions.resource_not_found_exception import ResourceNotFoundException
from backend.shared.exceptions.invalid_fields_exception import InvalidFieldsException
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.shared.constants.common_constants import PAGINATION_DEFAULT_PAGE_NUMBER, PAGINATION_DEFAULT_PAGE_SIZE


class PaginationServiceMixin:
    def paginate_queryset(
            self,
            queryset,
            page_number=PAGINATION_DEFAULT_PAGE_NUMBER,
            page_size=PAGINATION_DEFAULT_PAGE_SIZE
    ):
        paginator = Paginator(queryset, page_size)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = []

        if isinstance(page_obj, list):
            next_page = previous_page = None
            count = total_pages = 0
        else:
            next_page = page_obj.next_page_number() if page_obj.has_next() else None
            previous_page = page_obj.previous_page_number() if page_obj.has_previous() else None
            count = paginator.count
            total_pages = paginator.num_pages

        return {
            "page_obj": page_obj,
            "next_page": next_page,
            "previous_page": previous_page,
            "count": count,
            "total_pages": total_pages,
        }


class SerializationServiceMixin:
    serializer = None  # model serializer
    serializer2 = None  # response

    def serialize(self, instance, many=False):
        if self.serializer2:
            return self.serializer2(instance, many=many).data
        raise NotImplementedError("serializer2 not defined")

    def validate_and_serialize(self, data):
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            return serializer.validated_data
        raise InvalidFieldsException(
            message="Bad Request", fields=serializer.errors.items()
        )

    def validate_and_serialize_upd(self, instance, data):
        serializer = self.serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            return serializer.validated_data
        raise InvalidFieldsException(
            message="Bad Request", fields=serializer.errors.items()
        )


class FindServiceMixin:
    def find_all(self, filter=None, filter_params=None, order_by='id', order_by_direction='-'):
        queryset = self.model.objects.all()
        if filter_params:
            queryset = filter(filter_params, queryset=queryset).qs
            order_by = filter_params.get("order_by") or "id"
            order_by_direction = '' if filter_params.get(
                "order_by_asc") else '-'
        order_by_query = f"{order_by_direction}{order_by}"
        queryset = queryset.order_by(order_by_query)
        return queryset

    def find_one(self, pk):
        instance = self.model.objects.filter(pk=pk).first()
        if not instance:
            raise ResourceNotFoundException(
                message=f"Resource with id '{pk}' not found"
            )
        return instance

    def find_one_by_uuid(self, uuid):
        instance = self.model.objects.filter(uuid=uuid).first()
        if not instance:
            raise ResourceNotFoundException(
                message=f"Resource with uuid '{uuid}' not found"
            )
        return instance

    def find_one_by_attr(self, attr, value):
        instance = self.model.objects.filter(**{attr: value}).first()
        if not instance:
            raise ResourceNotFoundException(
                message=f"Resource with {attr} '{value}' not found"
            )
        return instance


class CreateUpdateServiceMixin:
    def create(self, data) -> dict:
        validated_data = self.validate_and_serialize(data)
        model_instance = self.model.objects.create(**validated_data)
        return self.serialize(model_instance)

    def update(self, pk, data) -> dict:
        # repeat logic 'cause some mixins find_one (service) error in args:
        instance = self.model.objects.filter(pk=pk).first()
        if not instance:
            raise ResourceNotFoundException(
                message=f"Resource with id '{pk}' not found"
            )
        validated_data = self.validate_and_serialize_upd(instance, data)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return self.serialize(instance)


class DeleteServiceMixin:
    def delete(self, pk):
        instance = self.model.objects.filter(pk=pk).first()
        if not instance:
            raise ResourceNotFoundException(
                message=f"Resource with id '{pk}' not found"
            )
        instance.delete()
