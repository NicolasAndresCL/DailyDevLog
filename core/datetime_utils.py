"""Utilidades de fecha/hora puras (stdlib `zoneinfo`, sin `pytz`)."""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

_TZ_CHILE = ZoneInfo("America/Santiago")


def formatear_fecha_chile(utc_str: str) -> str:
    """Convierte un ISO-8601 (UTC) a hora de Santiago con formato 'YYYY-MM-DD HH:MM'."""
    try:
        dt = datetime.fromisoformat(str(utc_str).replace("Z", "+00:00"))
        return dt.astimezone(_TZ_CHILE).strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return "Fecha inválida"
