from typing import Type

from backend.shared.services.base_service import BaseService

from multicpy.models.suscripcion_model import Suscripcion
from multicpy.filters.suscripcion_filters import SuscripcionFilter
from multicpy.serializers.suscripcion_serializers import (
    SuscripcionSerializer,
    SuscripcionResponseSerializer,
)


class SuscripcionService(BaseService):
    model: Type[Suscripcion]

    filter = Type[SuscripcionFilter]

    serializer = Type[SuscripcionSerializer]
    serializer2 = Type[SuscripcionResponseSerializer]

    def __init__(self, model):
        filter = SuscripcionFilter
        serializer = SuscripcionSerializer
        serializer2 = SuscripcionResponseSerializer
        super().__init__(model, filter, serializer, serializer2)
