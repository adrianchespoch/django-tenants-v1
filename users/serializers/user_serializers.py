from rest_framework import serializers

from backend.shared.serializers.serializers import (
    OptionalFieldsModelSerializer,
    FiltersBaseSerializer,
    QueryDocWrapperSerializer,
    QueryListDocWrapperSerializer
)
from backend.shared.utils.validators_utils import validate_password
from backend.shared.constants.choices import IDENTIFICATION_TYPE
from users.models.user_model import User


# ### User Serializer - Persist in db ===============
class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, help_text='Username')
    # Hacerlo opcional solo en la base si es común
    password = serializers.CharField(
        write_only=True, help_text='Password', required=True, validators=[validate_password])
    email = serializers.EmailField(help_text='Email')
    razon_social = serializers.CharField(
        max_length=200, help_text='Razón Social')
    tipo_identificacion = serializers.ChoiceField(
        choices=IDENTIFICATION_TYPE, help_text='Tipo de identificación')
    identificacion = serializers.CharField(
        max_length=20, help_text='Identificación')
    groups = serializers.ListField(
        child=serializers.IntegerField(), help_text='Grupos', required=False)


class UserCreateSerializer(BaseUserSerializer):
    def __init__(self, *args, **kwargs):
        super(UserCreateSerializer, self).__init__(*args, **kwargs)

    # creation validation
    def validate_username(self, value):
        sent_id = self.context.get('pk', None)  # controlled by view
        user = User.objects.filter(username=value).first()
        if user and (user.id != sent_id):
            raise serializers.ValidationError("Este username ya está en uso.")
        return value

    def validate_email(self, value):
        sent_id = self.context.get('pk', None)
        user = User.objects.filter(email=value).first()
        if user and (user.id != sent_id):
            raise serializers.ValidationError("Este email ya está en uso.")
        return value


# ### Filter Serializer - Get All ===============
class UserFilterSerializer(FiltersBaseSerializer):
    class Meta:
        model = User
        fields = '__all__'


# ### Response: Get All & Get By ID ===============
class UserResponseSerializer(OptionalFieldsModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(), required=False)

    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_superuser',
                   'last_login', 'created_at', 'modified_at', 'user_permissions']


# ### Swagger ===============
# ## Response Body: Post & Put & Patch

class UserOptDocWrapperSerializer(QueryDocWrapperSerializer):
    data = UserResponseSerializer(required=False)


# ## Get All Response Doc
class UserQueryDocWrapperSerializer(QueryListDocWrapperSerializer):
    data = UserResponseSerializer(many=True, required=False)
