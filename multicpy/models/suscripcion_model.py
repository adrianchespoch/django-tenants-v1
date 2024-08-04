import uuid
from django.db import models

from backend.shared.models.models import AuditDateModel


class Suscripcion(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    state = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True, max_length=801)

    olt_quantity = models.IntegerField(verbose_name='Cantidad de OLT')
    has_electronic_billing = models.BooleanField(
        default=False, verbose_name='Tiene Facturación Electrónica')
    invoice_quantity = models.IntegerField(
        default=0, verbose_name='Cantidad de Facturas')
    sales_ticket_quantity = models.IntegerField(
        default=0, verbose_name='Cantidad de Tickets de Venta')
    credit_note_quantity = models.IntegerField(
        default=0, verbose_name='Cantidad de Notas de Crédito')
    has_consumption_graphs = models.BooleanField(
        default=False, verbose_name='Tiene Gráficas de Consumo')
    has_monitoring = models.BooleanField(
        default=False, verbose_name='Tiene Monitoreo')
    price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio')
