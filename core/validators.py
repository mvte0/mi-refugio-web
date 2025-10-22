from django.core.exceptions import ValidationError


def normalize_rut(rut: str) -> str:
    if not rut:
        raise ValidationError("RUT requerido")
    s = rut.replace(".", "").replace(" ", "").replace("–", "-").replace("—", "-").upper()
    s = s.replace("-", "")
    if len(s) < 2:
        raise ValidationError("RUT inválido")
    body, dv = s[:-1], s[-1]
    if not body.isdigit():
        raise ValidationError("RUT inválido")

    # Cálculo dígito verificador (módulo 11)
    factors = [2, 3, 4, 5, 6, 7]
    acc = 0
    for i, ch in enumerate(reversed(body)):
        acc += int(ch) * factors[i % len(factors)]
    remainder = 11 - (acc % 11)
    if remainder == 11:
        dv_calc = "0"
    elif remainder == 10:
        dv_calc = "K"
    else:
        dv_calc = str(remainder)

    if dv != dv_calc:
        raise ValidationError("RUT inválido")
    # Almacenar sin puntos, con guion
    return f"{body}-{dv}"


def validate_rut(value: str):
    # Solo valida; lanza ValidationError si no pasa
    normalize_rut(value)

