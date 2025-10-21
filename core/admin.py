# core/admin.py
from django.contrib import admin
from .models import Sugerencia

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "creado", "nombre", "email", "short_msg")
    search_fields = ("nombre", "email", "mensaje")
    list_filter = ("creado",)

    def short_msg(self, obj):
        s = obj.mensaje or ""
        return (s[:60] + "…") if len(s) > 60 else s
    short_msg.short_description = "Mensaje"
