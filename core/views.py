# core/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest
import requests
from .models import Sugerencia

def landing(request):
    # Render de la landing
    return render(request, "index.html")

def api_sugerencias(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    nombre  = (request.POST.get("nombre") or "").strip()
    email   = (request.POST.get("email") or "").strip()
    mensaje = (request.POST.get("mensaje") or "").strip()
    tipo    = (request.POST.get("type")   or "").strip()
    token   = request.POST.get("g-recaptcha-response", "")

    if not (nombre and email and mensaje and token):
        messages.error(request, "Faltan datos o reCAPTCHA.")
        return redirect("/#contacto")

    # Validación reCAPTCHA
    try:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.RECAPTCHA_SECRET, "response": token},
            timeout=8
        )
        ok = r.json().get("success", False)
    except Exception:
        ok = False

    if not ok:
        messages.error(request, "No pudimos validar el reCAPTCHA. Intenta nuevamente.")
        return redirect("/#contacto")

    if tipo:
        mensaje = f"[{tipo.upper()}] {mensaje}"

    Sugerencia.objects.create(nombre=nombre, email=email, mensaje=mensaje)
    messages.success(request, "¡Gracias! Recibimos tu mensaje.")
    return redirect("/#contacto")
