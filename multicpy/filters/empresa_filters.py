from backend.shared.filters.filters import BaseFilter
from multicpy.models.empresa_model import Empresa


class EmpresaFilter(BaseFilter):
    class Meta:
        model = Empresa
        fields = '__all__'
