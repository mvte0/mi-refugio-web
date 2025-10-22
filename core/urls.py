# core/urls.py
from django.urls import path
from . import views
from . import views_auth

urlpatterns = [
    path("", views.landing, name="home"),
    path("api/sugerencias/", views.api_sugerencias, name="api_sugerencias"),
    path("registro/", views_auth.register, name="register"),
]
