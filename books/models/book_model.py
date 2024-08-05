import uuid
from django.db import models

from backend.shared.models.models import AuditDateModel


class Book(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    edition = models.PositiveIntegerField()
    isbn = models.CharField(max_length=255)
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=255)
    description = models.TextField()
