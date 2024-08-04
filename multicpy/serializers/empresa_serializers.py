from rest_framework import serializers

from backend.shared.serializers.serializers import (
    FiltersBaseSerializer,
    QueryDocWrapperSerializer,
    QueryListDocWrapperSerializer
)
from multicpy.models.empresa_model import Empresa


# ### Empresa Serializer - Model ===============
class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


# ## Response: Get All & Get By ID
class EmpresaResponseSerializer(FiltersBaseSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


# ### Filter Serializer - Get All ===============
class EmpresaFilterSerializer(FiltersBaseSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


# ### Swagger ===============
# ## Response Body: Post & Put & Patch
class EmpresaOptDocWrapperSerializer(QueryDocWrapperSerializer):
    data = EmpresaResponseSerializer(required=False)


# ## Get All Response
class EmpresaQueryDocWrapperSerializer(QueryListDocWrapperSerializer):
    data = EmpresaResponseSerializer(many=True, required=False)
