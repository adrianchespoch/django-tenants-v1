import uuid
from django.db import models

from backend.shared.models.models import AuditDateModel
from backend.shared.constants.choices import IDENTIFICATION_TYPE

from .suscripcion_model import Suscripcion

# ### tenancy ---------------
from backend import settings
import time
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import schema_rename


class Scheme(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def is_public(self):
        return self.name.lower() == 'public'


class Empresa(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    state = models.BooleanField(default=True)
    tipo_identificacion = models.CharField(
        max_length=100, choices=IDENTIFICATION_TYPE)
    identificacion = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=200)
    commercial_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=200)
    phone_1 = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    phone_3 = models.CharField(max_length=20, blank=True, null=True)

    logo_url = models.URLField(max_length=200, blank=True, null=True)
    is_agente_retencion = models.BooleanField(default=False)
    number_agente_retencion = models.IntegerField(default=0)

    razon_social_representante = models.CharField(
        max_length=200, blank=True, null=True)
    identificacion_representante = models.CharField(
        max_length=100, blank=True, null=True)
    email_representante = models.EmailField(
        max_length=200, blank=True, null=True)
    phone_representante = models.CharField(
        max_length=20, blank=True, null=True)
    contador = models.CharField(max_length=200, blank=True, null=True)
    genera_ats = models.BooleanField(default=False)

    # pais = models.ForeignKey(Pais, on_delete=models.SET_NULL,
    #                          related_name='empresa', null=True)
    # provincia = models.ForeignKey(
    #     Provincia, on_delete=models.SET_NULL, related_name='empresa', null=True)
    # ciudad = models.ForeignKey(
    #     Ciudad, on_delete=models.SET_NULL, related_name='empresa', null=True)

    suscripcion = models.ForeignKey(
        Suscripcion, on_delete=models.SET_NULL, null=True, verbose_name='Suscripcion/Plan para cada empresa')

    # ### tenants ------------
    scheme = models.OneToOneField(
        Scheme, on_delete=models.CASCADE, verbose_name='Esquema DB')
    schema_name = models.CharField(max_length=60, null=True, blank=True,
                                   help_text='Ingrese un nombre de esquema', verbose_name='Nombre del esquema')

    def create_schema(self):
        scheme = Scheme.objects.create(
            name=self.schema_name, schema_name=self.schema_name)
        Domain.objects.create(
            domain=f'{scheme.schema_name}.{settings.DOMAIN}', tenant=scheme, is_primary=True)
        return scheme

    def rename_schema(self):
        self.scheme.name = self.schema_name
        self.scheme.save()
        domain = self.scheme.get_primary_domain()
        schema_rename(self.scheme, self.schema_name)
        time.sleep(1)
        if domain:
            domain.domain = f'{self.scheme.schema_name}.{settings.DOMAIN}'
            domain.save()

    # ### Main CRUD operations ------------

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None or self.scheme is None:
            self.scheme = self.create_schema()
        else:
            scheme = Scheme.objects.get(pk=self.scheme.pk)
            if scheme.schema_name != self.schema_name:
                self.rename_schema()
        super(Empresa, self).save()


class Domain(DomainMixin):
    pass
