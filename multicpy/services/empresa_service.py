from typing import Type

from backend.shared.services.base_service import BaseService

from multicpy.models.empresa_model import Empresa
from multicpy.filters.empresa_filters import EmpresaFilter
from multicpy.serializers.empresa_serializers import (
    EmpresaSerializer,
    EmpresaResponseSerializer,
)


class EmpresaService(BaseService):
    model: Type[Empresa]

    filter = Type[EmpresaFilter]

    serializer = Type[EmpresaSerializer]
    serializer2 = Type[EmpresaResponseSerializer]

    def __init__(self, model):
        filter = EmpresaFilter
        serializer = EmpresaSerializer
        serializer2 = EmpresaResponseSerializer
        super().__init__(model, filter, serializer, serializer2)
