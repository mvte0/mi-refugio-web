from django.db import models


class Donation(models.Model):
    """Registro de donaciones realizadas a traves de Webpay."""

    cliente = models.ForeignKey(
        "core.Cliente",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="donations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    buy_order = models.CharField(max_length=60, unique=True)
    session_id = models.CharField(max_length=60)
    token_ws = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=30,
        default="initialized",
        help_text="Estados: initialized, authorized, failed, aborted.",
    )
    authorization_code = models.CharField(max_length=40, blank=True)
    payment_type = models.CharField(max_length=10, blank=True)
    installments_number = models.IntegerField(null=True, blank=True)
    response_raw = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.buy_order} - {self.amount}"
