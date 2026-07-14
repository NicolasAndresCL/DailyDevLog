"""Configuración del cliente de escritorio.

La URL base de la API se lee de la variable de entorno ``DAILYDEVLOG_API_URL``
(por defecto ``http://localhost:8000``), para poder apuntar a la API desplegada
sin tocar el código. Ver skill.md §1 (no hardcodear config).
"""
import os

API_BASE_URL = os.environ.get("DAILYDEVLOG_API_URL", "http://localhost:8000").rstrip("/")
API_URL = f"{API_BASE_URL}/api/dailylog/"
MEDIA_URL_BASE = API_BASE_URL
