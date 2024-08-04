import os
from django.db import transaction
from django.contrib.auth.hashers import make_password  # hashear password


from users.models.user_model import User


def seed_users():
    # admin users list:
    admin_users = [
        {
            'username': 'admin2',
            'password': 'Admin123.',
            'razon_social': 'Admin 2',
            'email': 'admin2@demo.com',
            "is_staff": True,
            "is_superuser": True,
            'tipo_identificacion': 'CEDULA',
            'identificacion': '123456789',
        },
        {
            'username': 'admin3',
            'password': 'Admin123.',
            'razon_social': 'Admin 3',
            'email': 'admin3@demo.com',
            "is_staff": True,
            "is_superuser": True,
            'tipo_identificacion': 'CEDULA',
            'identificacion': '123456789',
        },
        {
            'username': 'admin4',
            'password': 'Admin123.',
            'razon_social': 'Admin 4',
            'email': 'admin4@demo.com',
            "is_staff": True,
            "is_superuser": True,
            'tipo_identificacion': 'CEDULA',
            'identificacion': '123456789',
        },
        {
            'username': 'admin5',
            'password': 'Admin123.',
            'razon_social': 'Admin 5',
            'email': 'admin5@demo.com',
            "is_staff": True,
            "is_superuser": True,
            'tipo_identificacion': 'CEDULA',
            'identificacion': '123456789',
        },
    ]

    with transaction.atomic():
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

        # Crea los usuarios admin if not exists
        for admin in admin_users:
            if not User.objects.filter(username=admin['username']).exists():
                user = User.objects.create(
                    username=admin['username'],
                    password=make_password(admin['password']),
                    razon_social=admin['razon_social'],
                    email=admin['email'],
                    is_staff=admin['is_staff'],
                    is_superuser=admin['is_superuser'],
                )
    print("Users seed completed.")
