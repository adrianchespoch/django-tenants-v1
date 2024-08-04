import json
import os

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

# tenants
from django_tenants.utils import schema_context
from multicpy.models import Scheme, Domain, Suscripcion
from backend import settings

# auth
from users.models.extended_group_model import ExtendedGroup
from users.models.user_model import User
from django.contrib.auth.models import Permission

# other
from users.shared.constants.system_modules import system_modules_sidenav


class Command(BaseCommand):
    help = 'Allows to initiate the base software installation'

    def load_json_from_file(self, file):
        with open(f'{settings.BASE_DIR}/multicpy/shared/admin/jsons/{file}', 'r') as wr:
            return json.loads(wr.read())

    def handle(self, *args, **options):
        scheme = Scheme.objects.get_or_create(
            name=settings.DEFAULT_SCHEMA, schema_name=settings.DEFAULT_SCHEMA)[0]
        Domain.objects.get_or_create(
            domain=settings.DOMAIN, tenant=scheme, is_primary=True)
        with schema_context(scheme.schema_name):
            # ## Suscripciones ==============================
            for suscripcion_json in self.load_json_from_file(file='subscriptions.json'):
                Suscripcion.objects.create(**suscripcion_json)

            # ## Grupos & Permissions ==============================
            group = ExtendedGroup.objects.create(
                name='Administrador', system_modules=system_modules_sidenav)
            print(f'insertado {group.name}')
            group.permissions.set(Permission.objects.all())

            # ## Users ==============================
            # Verifica si ya existe un usuario con el username dado
            if not User.objects.filter(username=os.environ.get("ADMIN_USERNAME")).exists():
                # Si no existe, procede a crear o actualizar el usuario
                user, created = User.objects.update_or_create(
                    email=os.environ.get("ADMIN_EMAIL"),
                    defaults={
                        'username': os.environ.get("ADMIN_USERNAME"),
                        'password': make_password(os.environ.get("ADMIN_PASSWORD")),
                        'razon_social': os.environ.get("ADMIN_RAZON_SOCIAL"),
                        'is_staff': True,
                        'is_superuser': True,
                    }
                )
            else:
                print(
                    f"El usuario con username {os.environ.get('ADMIN_USERNAME')} ya existe.")
