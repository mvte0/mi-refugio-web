from django.contrib import admin
from django.utils.html import format_html

from .models import Cliente, Sugerencia


@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "creado", "nombre", "email", "short_msg")
    search_fields = ("nombre", "email", "mensaje")
    list_filter = ("creado",)

    def short_msg(self, obj):
        message = obj.mensaje or ""
        return (message[:60] + "...") if len(message) > 60 else message

    short_msg.short_description = "Mensaje"


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "creado", "user", "rut", "avatar_preview")
    search_fields = ("user__username", "user__email", "rut")
    list_filter = ("creado",)

    def avatar_preview(self, obj):
        if not obj.avatar:
            return "—"
        return format_html(
            '<img src="{}" alt="{}" style="height:48px;border-radius:50%;">',
            obj.avatar.url,
            obj.user.username,
        )

    avatar_preview.short_description = "Avatar"
