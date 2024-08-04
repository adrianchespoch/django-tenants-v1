from rest_framework import serializers

from backend.shared.serializers.serializers import (
    FiltersBaseSerializer,
    QueryDocWrapperSerializer,
    QueryListDocWrapperSerializer
)
from multicpy.models.suscripcion_model import Suscripcion


# ### Suscripcion Serializer - Model ===============
class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'


# ## Response: Get All & Get By ID
class SuscripcionResponseSerializer(FiltersBaseSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'


# ### Filter Serializer - Get All ===============
class SuscripcionFilterSerializer(FiltersBaseSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'


# ### Swagger ===============
# ## Response Body: Post & Put & Patch
class SuscripcionOptDocWrapperSerializer(QueryDocWrapperSerializer):
    data = SuscripcionResponseSerializer(required=False)


# ## Get All Response
class SuscripcionQueryDocWrapperSerializer(QueryListDocWrapperSerializer):
    data = SuscripcionResponseSerializer(many=True, required=False)
