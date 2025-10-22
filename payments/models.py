from django.db import models
from django.conf import settings

# Create your models here.
class Donation(models.Model):
    # Enlaza la donación al cliente autenticado que la inicia
    # (nullable para compatibilidad con registros existentes)
    from django.apps import apps
    # Referencia diferida a evitar import circular
    cliente = models.ForeignKey('core.Cliente', null=True, blank=True, on_delete=models.SET_NULL, related_name='donations')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    buy_order = models.CharField(max_length=60, unique=True)
    session_id = models.CharField(max_length=60)
    token_ws = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=30, default="initialized")  # initialized, authorized, failed, aborted
    authorization_code = models.CharField(max_length=40, blank=True)
    payment_type = models.CharField(max_length=10, blank=True)
    installments_number = models.IntegerField(null=True, blank=True)
    response_raw = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.buy_order} - {self.amount}"
