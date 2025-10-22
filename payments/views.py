import uuid, decimal
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseBadRequest
from .models import Donation

from transbank.webpay.webpay_plus.transaction import Transaction

# ===== IMPORTS COMPATIBLES CON transbank-sdk 5.x/6.x (y fallback 4.x) =====
try:
    # SDK 5.x / 6.x
    from transbank.common.options import Options
    from transbank.common.integration_type import IntegrationType
    from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
    from transbank.common.integration_api_keys import IntegrationApiKeys
except ImportError:
    # SDK 4.x (compatibilidad)
    from transbank.common import Options, IntegrationCommerceCodes, IntegrationApiKeys, IntegrationType
# ==========================================================================
def webpay_init(request):
    # Alias que reusa el POST del formulario de donaciÃ³n
    if request.method == "POST":
        return donate_form(request)
    # Si llegan por GET, muÃ©strales el form para que indiquen monto y datos
    return render(request, "donations/form.html")

def _tbk_options():
    """Configura el SDK según ambiente y credenciales."""
    if getattr(settings, 'TBK_ENV', 'integration') == "production":
        return Options(settings.TBK_API_KEY_ID, settings.TBK_API_KEY_SECRET, IntegrationType.LIVE)
    # integración (sandbox)
    return Options(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)

@csrf_protect
@login_required(login_url='login')
def donate_form(request):
    if request.method == "GET":
        return render(request, "donations/form.html")

    try:
        amount = decimal.Decimal(request.POST.get("amount", "0")).quantize(decimal.Decimal("1."))
    except Exception:
        return HttpResponseBadRequest("Monto invÃ¡lido")

    if amount < 500:
        return HttpResponseBadRequest("El monto mÃ­nimo es $500")

    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    message = request.POST.get("message", "")

    buy_order = f"MR-{timezone.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    session_id = uuid.uuid4().hex[:12]

    # Asociar cliente si existe
    cliente = getattr(getattr(request.user, 'cliente', None), 'id', None)
    donation = Donation.objects.create(
        cliente=request.user.cliente if hasattr(request.user, 'cliente') else None,
        amount=amount, name=name, email=email, message=message,
        buy_order=buy_order, session_id=session_id
    )

    tx = Transaction(_tbk_options())
    resp = tx.create(buy_order, session_id, int(amount), settings.TBK_RETURN_URL)
    token = resp.get("token")
    url = resp.get("url")
    donation.token_ws = token
    donation.save(update_fields=["token_ws"])

    return redirect(f"{url}?token_ws={token}")

def webpay_return(request):
    token = request.POST.get("token_ws") or request.GET.get("token_ws")
    tbk_token = request.POST.get("TBK_TOKEN")
    tbk_orden_compra = request.POST.get("TBK_ORDEN_COMPRA")
    tbk_id_sesion = request.POST.get("TBK_ID_SESION")

    # Aborto/cancelaciÃ³n
    if tbk_token or tbk_orden_compra or tbk_id_sesion:
        if tbk_orden_compra:
            Donation.objects.filter(buy_order=tbk_orden_compra).update(status="aborted")
        return render(request, "donations/result.html", {"ok": False, "aborted": True})

    if not token:
        return HttpResponseBadRequest("Token faltante")

    tx = Transaction(_tbk_options())
    result = tx.commit(token)

    buy_order = result.get("buy_order")
    status = (result.get("status") or "").upper()
    ok = (status == "AUTHORIZED")

    Donation.objects.filter(buy_order=buy_order).update(
        status="authorized" if ok else (status or "failed").lower(),
        authorization_code=result.get("authorization_code") or "",
        payment_type=result.get("payment_type_code") or "",
        installments_number=result.get("installments_number"),
        response_raw=result
    )
    return render(request, "donations/result.html", {"ok": ok, "result": result})

# --- Ajuste SDK: asegurar Options concretas en integración (SDK 6.x usa WebpayOptions) ---
try:
    from transbank.common.options import WebpayOptions as _TBKOptions
except Exception:
    try:
        from transbank.common.options import Options as _TBKOptions
    except Exception:
        from transbank.common import Options as _TBKOptions

def _tbk_options():
    if getattr(settings, 'TBK_ENV', 'integration') == 'production':
        return _TBKOptions(settings.TBK_API_KEY_ID, settings.TBK_API_KEY_SECRET, IntegrationType.LIVE)
    # Integración por defecto con códigos/keys del SDK
    return _TBKOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)



def webpay_status(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponseBadRequest("Falta token")
    tx = Transaction(_tbk_options())
    try:
        data = tx.status(token)
        from django.http import JsonResponse
        return JsonResponse(data)
    except Exception as e:
        from django.http import JsonResponse
        return JsonResponse({"error": str(e)}, status=400)
