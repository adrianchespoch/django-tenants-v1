import uuid
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from backend.shared.models.models import AuditDateModel


# ### Custom User Model: debemos registrarlo en Django para q lo use en lugar del x default
class CustomUserManager(UserManager):
    def _create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("Invalid email")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)  # is_staff false = NO Admin
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # is_staff true = Admin
        # is_superuser true = Superuser
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    razon_social = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)  # active

    is_staff = models.BooleanField(default=False)  # admin?
    objects = CustomUserManager()  #

    # USERNAME_FIELD = "username"  # django username = username
    # REQUIRED_FIELDS = ["email", "razon_social"]  # Campos adicionales requeridos (createsuperuser)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # ## Other fields ----------
    failed_login_attempts = models.IntegerField(default=0)
    ip_login = models.GenericIPAddressField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        # ordering = ["-created_at"]
        # indexes = [models.Index(fields=["email"])]  # create index for email
