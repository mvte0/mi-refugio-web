# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="home"),
    path("api/sugerencias/", views.api_sugerencias, name="api_sugerencias"),
]
