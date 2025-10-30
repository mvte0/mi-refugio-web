from django.core.exceptions import ValidationError


def normalize_rut(rut: str) -> str:
    """
    Normaliza un RUT chileno eliminando separadores y validando su digito verificador.
    Devuelve el valor en formato XXXXXXXX-D.
    """
    if not rut:
        raise ValidationError("RUT requerido")

    separators = {"-", "\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2212"}
    cleaned = []
    for char in rut.strip():
        if char in {" ", "."}:
            continue
        if char in separators:
            continue
        cleaned.append(char)

    normalized = "".join(cleaned).upper()
    if len(normalized) < 2:
        raise ValidationError("RUT invalido")

    body, dv = normalized[:-1], normalized[-1]
    if not body.isdigit():
        raise ValidationError("RUT invalido")

    factors = [2, 3, 4, 5, 6, 7]
    acc = 0
    for index, digit in enumerate(reversed(body)):
        acc += int(digit) * factors[index % len(factors)]
    remainder = 11 - (acc % 11)

    if remainder == 11:
        dv_expected = "0"
    elif remainder == 10:
        dv_expected = "K"
    else:
        dv_expected = str(remainder)

    if dv != dv_expected:
        raise ValidationError("RUT invalido")

    return f"{body}-{dv}"


def validate_rut(value: str) -> None:
    """Valida que el RUT sea correcto, lanzando ValidationError si no es valido."""
    normalize_rut(value)
