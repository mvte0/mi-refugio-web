from django.conf import settings


def project_settings(request):
    """Expone configuraciones basicas necesarias en las plantillas."""
    return {
        "recaptcha_site_key": getattr(settings, "RECAPTCHA_SITE_KEY", ""),
        "donation_min_amount": getattr(settings, "DONATION_MIN_CLP", 500),
    }
