from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from .validators import validate_rut

# Create your models here.
class Sugerencia(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    nombre  = models.CharField(max_length=120)
    email   = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return f"{self.nombre} <{self.email}> ({self.creado:%Y-%m-%d})"


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")
    rut = models.CharField(max_length=14, unique=True, null=True, blank=True, validators=[validate_rut])
    avatar = models.FileField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif", "webp"])],
    )
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cliente #{self.id} - {self.user.username} ({self.rut})"
