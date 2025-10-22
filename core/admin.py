# core/admin.py
from django.contrib import admin
from .models import Sugerencia, Cliente

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "creado", "nombre", "email", "short_msg")
    search_fields = ("nombre", "email", "mensaje")
    list_filter = ("creado",)

    def short_msg(self, obj):
        s = obj.mensaje or ""
        return (s[:60] + "…") if len(s) > 60 else s
    short_msg.short_description = "Mensaje"


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "creado", "user", "rut")
    search_fields = ("user__username", "user__email", "rut")
    list_filter = ("creado",)
