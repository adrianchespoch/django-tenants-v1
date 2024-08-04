from rest_framework import serializers

from backend.shared.serializers.serializers import (
    FiltersBaseSerializer,
    QueryDocWrapperSerializer,
    QueryListDocWrapperSerializer
)
from users.models.extended_group_model import ExtendedGroup


# ### ExtendedGroup Serializer - Model ===============
class ExtendedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedGroup
        fields = '__all__'


# ## Response: Get All & Get By ID
class ExtendedGroupResponseSerializer(FiltersBaseSerializer):
    class Meta:
        model = ExtendedGroup
        fields = '__all__'


# ### Filter Serializer - Get All ===============
class ExtendedGroupFilterSerializer(FiltersBaseSerializer):
    class Meta:
        model = ExtendedGroup
        fields = '__all__'


# ### Swagger ===============
# ## Response Body: Post & Put & Patch
class ExtendedGroupOptDocSerializer(FiltersBaseSerializer):
    class Meta:
        model = ExtendedGroup
        fields = '__all__'

class ExtendedGroupOptDocWrapperSerializer(QueryDocWrapperSerializer):
    data = ExtendedGroupResponseSerializer(required=False)


# ## Get All Response
class ExtendedGroupQueryDocWrapperSerializer(QueryListDocWrapperSerializer):
    data = ExtendedGroupResponseSerializer(many=True, required=False)
