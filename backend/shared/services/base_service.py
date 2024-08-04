from backend.shared.services.base_mixin_service import PaginationServiceMixin, SerializationServiceMixin, FindServiceMixin, CreateUpdateServiceMixin, DeleteServiceMixin
from backend.shared.constants.common_constants import PAGINATION_DEFAULT_PAGE_NUMBER, PAGINATION_DEFAULT_PAGE_SIZE


class BaseService(PaginationServiceMixin, SerializationServiceMixin, FindServiceMixin, CreateUpdateServiceMixin):
    # DI model | others just args
    def __init__(self, model, filter=None, serializer=None, serializer2=None):
        self.model = model
        self.filter = filter
        self.serializer = serializer
        self.serializer2 = serializer2

    def find_all(self, filter_params=None, page_number=PAGINATION_DEFAULT_PAGE_NUMBER, page_size=PAGINATION_DEFAULT_PAGE_SIZE):
        queryset = FindServiceMixin.find_all(self,
                                             self.filter, filter_params)
        paginated_data = self.paginate_queryset(
            queryset, page_number, page_size)
        serialized_data = self.serialize(paginated_data["page_obj"], many=True)
        return {
            "meta": {
                "next": paginated_data["next_page"],
                "previous": paginated_data["previous_page"],
                "count": paginated_data["count"],
                "total_pages": paginated_data["total_pages"],
            },
            "data": serialized_data,
        }

    def find_one(self, pk) -> dict:
        instance = FindServiceMixin.find_one(self, pk)
        return self.serialize(instance)

    def find_one_by_uuid(self, uuid) -> dict:
        instance = FindServiceMixin.find_one_by_uuid(
            self, uuid)
        return self.serialize(instance)

    def find_one_by_attr(self, attr: str, value) -> dict:
        instance = FindServiceMixin.find_one_by_attr(
            self, attr, value)
        return self.serialize(instance)

    def create(self, data) -> dict:
        return CreateUpdateServiceMixin.create(self, data)

    def update(self, pk, data) -> dict:
        return CreateUpdateServiceMixin.update(self, pk, data)


class BaseServiceAll(PaginationServiceMixin, SerializationServiceMixin, FindServiceMixin, CreateUpdateServiceMixin, DeleteServiceMixin):
    def __init__(self, model, filter=None, serializer=None, serializer2=None):
        self.model = model
        self.filter = filter
        self.serializer = serializer
        self.serializer2 = serializer2

    def find_all(self, filter_params=None, page_number=PAGINATION_DEFAULT_PAGE_NUMBER, page_size=PAGINATION_DEFAULT_PAGE_SIZE):
        queryset = FindServiceMixin.find_all(self, self.filter, filter_params)
        paginated_data = self.paginate_queryset(
            queryset, page_number, page_size)
        serialized_data = self.serialize(paginated_data["page_obj"], many=True)
        return {
            "meta": {
                "next": paginated_data["next_page"],
                "previous": paginated_data["previous_page"],
                "count": paginated_data["count"],
                "total_pages": paginated_data["total_pages"],
            },
            "data": serialized_data,
        }

    def find_one(self, pk) -> dict:
        instance = FindServiceMixin.find_one(self, pk)
        return self.serialize(instance)

    def find_one_by_uuid(self, uuid) -> dict:
        instance = FindServiceMixin.find_one_by_uuid(
            self, uuid)
        return self.serialize(instance)

    def find_one_by_attr(self, attr: str, value) -> dict:
        instance = FindServiceMixin.find_one_by_attr(
            self, attr, value)
        return self.serialize(instance)

    def create(self, data) -> dict:
        return CreateUpdateServiceMixin.create(self, data)

    def update(self, pk, data) -> dict:
        return CreateUpdateServiceMixin.update(self, pk, data)
