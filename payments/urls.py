from django.urls import path
from . import views

urlpatterns = [
    path("donar/", views.donate_form, name="donate_form"),
    path("pagos/retorno/", views.webpay_return, name="webpay_return"),
    path("pagos/estado/", views.webpay_status, name="webpay_status"),
]
