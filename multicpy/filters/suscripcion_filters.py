from backend.shared.filters.filters import BaseFilter
from multicpy.models.suscripcion_model import Suscripcion


class SuscripcionFilter(BaseFilter):
    class Meta:
        model = Suscripcion
        fields = '__all__'
