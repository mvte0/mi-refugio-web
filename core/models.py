from django.db import models

# Create your models here.
class Sugerencia(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    nombre  = models.CharField(max_length=120)
    email   = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return f"{self.nombre} <{self.email}> ({self.creado:%Y-%m-%d})"