from django.contrib import admin
from .models import Sugerencia

# Register your models here.
@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre","email","creado")
    search_fields = ("nombre","email","mensaje")
    list_filter = ("creado",)