import json

from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context

# ###
from multicpy.models import Empresa
from users.models import User
from backend import settings
from django.contrib.auth.hashers import make_password



class Command(BaseCommand):
    help = 'Allows to execute commands'

    def add_arguments(self, parser):
        parser.add_argument('--schema_name', nargs='?', type=str,
                            default='sometest1', help='Nombre del esquema')

    def load_json_from_file(self, file):
        with open(f'{settings.BASE_DIR}/multicpy/shared/company/jsons/{file}', 'r') as wr:
            return json.loads(wr.read())

    def handle(self, *args, **options):
        empresa = Empresa.objects.create(
            state=True,
            tipo_identificacion='RUC',
            identificacion="1234567890",
            razon_social="Empresa Ejemplo S.A.",
            commercial_name="Ejemplo Comercial",
            email="contacto@ejemplo.com",
            address="Calle Falsa 123, Ciudad Ejemplo",
            phone_1="+593987654321",
            phone_2="+593987654322",
            phone_3="+593987654323",
            logo_url="https://www.ejemplo.com/logo.png",
            is_agente_retencion=False,
            number_agente_retencion=0,
            razon_social_representante="Juan Pérez",
            identificacion_representante="0987654321",
            email_representante="juan.perez@ejemplo.com",
            phone_representante="+593987654324",
            contador="María Gómez",
            genera_ats=True,

            suscripcion_id=1,
            schema_name=options['schema_name'],
        )

        with schema_context(empresa.scheme.schema_name):
            # ## Users ==============================
            for user_object in self.load_json_from_file(file='users.json'):
                # Verifica si ya existe un usuario con el username dado
                if not User.objects.filter(username=user_object['username']).exists():
                    # Si no existe, procede a crear o actualizar el usuario
                    user, created = User.objects.update_or_create(
                        email=user_object['email'],
                        defaults={
                            'username': user_object['username'],
                            'password': make_password(user_object['password']),
                            'razon_social': user_object['razon_social'],
                            'is_staff': user_object['is_staff'],
                            'is_superuser': user_object['is_superuser'],
                        }
                    )

        self.stdout.write(self.style.SUCCESS(
            '[USERS]: Successfully seeded development database'))
