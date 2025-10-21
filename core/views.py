# core/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest
import requests
from .models import Sugerencia
import os, logging

def landing(request):
    # Render de la landing
    return render(request, "index.html")

logger = logging.getLogger(__name__)

def api_sugerencias(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    nombre  = (request.POST.get("nombre") or "").strip()
    email   = (request.POST.get("email") or "").strip()
    mensaje = (request.POST.get("mensaje") or "").strip()
    tipo    = (request.POST.get("type")   or "").strip()
    token   = request.POST.get("g-recaptcha-response", "")

    if not (nombre and email and mensaje):
        messages.error(request, "Faltan datos obligatorios.")
        return redirect("/#contacto")

    # Bypass temporal (para probar en Render)
    bypass = getattr(settings, "CONTACT_BYPASS_RECAPTCHA", False) or os.environ.get("CONTACT_BYPASS_RECAPTCHA") == "1"

    ok = True
    if not bypass:
        if not token:
            messages.error(request, "Falta reCAPTCHA.")
            return redirect("/#contacto")
        try:
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={"secret": settings.RECAPTCHA_SECRET, "response": token},
                timeout=8
            )
            resp = r.json()
            ok = resp.get("success", False)
            logger.info("reCAPTCHA resp: %s", resp)
        except Exception as e:
            logger.exception("Error validando reCAPTCHA")
            ok = False

    if not ok:
        messages.error(request, "No pudimos validar el reCAPTCHA. Intenta nuevamente.")
        return redirect("/#contacto")

    if tipo:
        mensaje = f"[{tipo.upper()}] {mensaje}"

    obj = Sugerencia.objects.create(nombre=nombre, email=email, mensaje=mensaje)
    logger.info("Sugerencia guardada id=%s", obj.id)

    messages.success(request, "¡Gracias! Recibimos tu mensaje.")
    return redirect("/#contacto")
