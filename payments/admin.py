from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("buy_order","amount","status","created_at","authorization_code","cliente")
    search_fields = ("buy_order","email","name","cliente__user__username","cliente__rut")
    list_filter = ("status","created_at")

