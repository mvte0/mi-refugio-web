import logging
import os

import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .models import Sugerencia

logger = logging.getLogger(__name__)
CONTACT_SECTION = "/#contacto"


def landing(request):
    """Pantalla principal del sitio."""
    context = {
        "recaptcha_site_key": getattr(settings, "RECAPTCHA_SITE_KEY", ""),
        "contact_bypass_recaptcha": getattr(settings, "CONTACT_BYPASS_RECAPTCHA", False),
    }
    return render(request, "index.html", context)


def acerca(request):
    """Pagina estatica con informacion del proyecto."""
    return render(request, "acerca.html")


def perfil(request):
    """Ficha resumida del perfil de usuario."""
    return render(request, "perfil.html")


def api_sugerencias(request):
    """Recibe el formulario de contacto, valida reCAPTCHA y guarda la sugerencia."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    nombre = (request.POST.get("nombre") or "").strip()
    email = (request.POST.get("email") or "").strip()
    mensaje = (request.POST.get("mensaje") or "").strip()
    tipo = (request.POST.get("type") or "").strip()
    token = request.POST.get("g-recaptcha-response", "")

    if not (nombre and email and mensaje):
        messages.error(request, "Faltan datos obligatorios.")
        return redirect(CONTACT_SECTION)

    bypass_flag = getattr(settings, "CONTACT_BYPASS_RECAPTCHA", False)
    bypass_env = os.environ.get("CONTACT_BYPASS_RECAPTCHA", "").strip().lower()
    bypass = bypass_flag or bypass_env in {"1", "true", "yes"}

    recaptcha_secret = (
        getattr(settings, "RECAPTCHA_SECRET", "")
        or os.environ.get("RECAPTCHA_SECRET", "")
    )

    should_verify = not bypass and bool(recaptcha_secret)
    if not recaptcha_secret and not bypass:
        logger.warning("No RECAPTCHA_SECRET configured; skipping verification.")
        should_verify = False

    if should_verify:
        if not token:
            messages.error(request, "Falta reCAPTCHA.")
            return redirect(CONTACT_SECTION)
        try:
            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={"secret": recaptcha_secret, "response": token},
                timeout=8,
            )
            response.raise_for_status()
            payload = response.json()
            if not payload.get("success", False):
                messages.error(request, "No pudimos validar el reCAPTCHA. Intenta de nuevo.")
                logger.info("reCAPTCHA failed: %s", payload)
                return redirect(CONTACT_SECTION)
        except requests.RequestException:
            logger.exception("Error validando reCAPTCHA.")
            messages.error(request, "Servicio de reCAPTCHA no disponible. Intenta mas tarde.")
            return redirect(CONTACT_SECTION)

    if tipo:
        mensaje = f"[{tipo.upper()}] {mensaje}"

    if len(mensaje) < 10:
        messages.error(request, "El mensaje debe tener al menos 10 caracteres.")
        return redirect(CONTACT_SECTION)

    Sugerencia.objects.create(nombre=nombre, email=email, mensaje=mensaje)
    messages.success(request, "Gracias. Recibimos tu mensaje.")
    return redirect(CONTACT_SECTION)
