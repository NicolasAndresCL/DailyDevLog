"""Agregación de estadísticas de productividad.

Lógica pura: sin red, sin Qt, sin pandas → testeable en aislamiento (skill.md §2.1).
Consume la lista de logs (dicts de la API) y devuelve estructuras simples que la GUI
convierte a gráficos.
"""
from __future__ import annotations

from datetime import datetime


def _parse_fecha(valor: object) -> datetime | None:
    if not valor:
        return None
    try:
        return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
    except ValueError:
        return None


def _franja(hora: int) -> str:
    if hora <= 12:
        return "mañana"
    if hora <= 18:
        return "tarde"
    return "noche"


def compute_stats(logs: list[dict]) -> dict:
    """Agrega logs en estadísticas de productividad.

    Devuelve ``{"empty": True}`` o::

        {"por_franja": [{"dia": str, "parte": str, "horas": float}, ...],
         "top_tecnologias": [{"tecnologia": str, "horas": float}, ...]}

    Las horas de una tarea se atribuyen a cada tecnología que declara (el campo
    ``tecnologias_utilizadas`` es un CSV; se separa por coma antes de agregar).
    """
    por_franja: dict[tuple[str, str], float] = {}
    por_tecnologia: dict[str, float] = {}

    for log in logs:
        horas_raw = log.get("horas")
        if horas_raw is None:
            continue
        try:
            horas = float(horas_raw)
        except (TypeError, ValueError):
            continue

        fecha = _parse_fecha(log.get("fecha_creacion"))
        if fecha is not None:
            clave = (fecha.date().isoformat(), _franja(fecha.hour))
            por_franja[clave] = por_franja.get(clave, 0.0) + horas

        for tec in str(log.get("tecnologias_utilizadas") or "").split(","):
            tec = tec.strip()
            if tec:
                por_tecnologia[tec] = por_tecnologia.get(tec, 0.0) + horas

    if not por_franja and not por_tecnologia:
        return {"empty": True}

    por_franja_list = [
        {"dia": dia, "parte": parte, "horas": horas}
        for (dia, parte), horas in sorted(por_franja.items())
    ]
    top = sorted(por_tecnologia.items(), key=lambda kv: kv[1], reverse=True)[:10]
    top_tecnologias = [{"tecnologia": t, "horas": h} for t, h in top]

    return {"por_franja": por_franja_list, "top_tecnologias": top_tecnologias}
