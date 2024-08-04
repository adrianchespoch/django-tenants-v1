import uuid
from django.db import models

from django.contrib.auth.models import Group

from backend.shared.utils.validators_utils import string_array_model_validator


class ExtendedGroup(Group):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(blank=True, null=True)
    system_modules = models.JSONField(
        blank=True, null=True, validators=[string_array_model_validator])

    class Meta:
        verbose_name = "Extended Group"
        verbose_name_plural = "Extended Groups"
