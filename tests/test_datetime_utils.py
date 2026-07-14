import re

from core.datetime_utils import formatear_fecha_chile


def test_utc_a_santiago():
    out = formatear_fecha_chile("2025-08-21T12:00:00Z")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", out)
    # Agosto: Santiago está en UTC-4 → 12:00Z = 08:00 local, mismo día.
    assert out.startswith("2025-08-21")


def test_fecha_invalida():
    assert formatear_fecha_chile("no-es-fecha") == "Fecha inválida"
    assert formatear_fecha_chile("") == "Fecha inválida"
