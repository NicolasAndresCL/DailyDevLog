"""Exportación de una tarea a Markdown.

Lógica pura (stdlib): acepta un modelo Django o un dict serializado y escribe un
`.md`. Movido desde `desktop_ui/export/` a la capa `core` (skill.md §2.1).
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


def _slug(nombre: str) -> str:
    """Nombre de archivo seguro (evita path traversal): solo letras, dígitos y `-`/`_`."""
    slug = re.sub(r"[^\w\-]", "_", nombre.strip().replace(" ", "_"))
    return slug or "tarea"


def exportar_a_markdown(log, ruta_destino: Path) -> Path:
    # Soporta dicts (API) o modelos Django.
    def get(attr):
        return getattr(log, attr, None) if hasattr(log, attr) else log.get(attr)

    fecha_raw = get("fecha_creacion")
    fecha = (
        fecha_raw.strftime("%Y-%m-%d")
        if isinstance(fecha_raw, datetime)
        else str(fecha_raw)[:10]
    )
    nombre_tarea = get("nombre_tarea") or "tarea"
    nombre_archivo = f"{_slug(fecha)}_{_slug(nombre_tarea)}.md"
    ruta_destino.mkdir(exist_ok=True, parents=True)
    ruta_completa = ruta_destino / nombre_archivo

    contenido = [
        f"# {nombre_tarea}",
        "",
        f"**Fecha:** {fecha}",
        f"**Horas trabajadas:** {get('horas')}",
        f"**Tecnologías utilizadas:** {get('tecnologias_utilizadas')}",
        "",
        "---",
        "",
        "## Descripción",
        "",
        get("descripcion") or "",
        "",
        "---",
        "",
        "## Links técnicos",
        "",
        f"- [Publicación en LinkedIn]({get('link_publicacion_linkedin')})" if get("link_publicacion_linkedin") else "",
        f"- [IA principal]({get('link_ia_principal')})" if get("link_ia_principal") else "",
        f"- [IA secundaria]({get('link_ia_secundaria')})" if get("link_ia_secundaria") else "",
        f"- [IA terciaria]({get('link_ia_terciaria')})" if get("link_ia_terciaria") else "",
        f"- [Repositorio]({get('link_respositorio')})" if get("link_respositorio") else "",
        f"- Commit: `{get('commit_principal')}`" if get("commit_principal") else "",
        "",
        "---",
        "",
        "## Imágenes",
        "",
    ]

    for i in range(1, 4):
        imagen = get(f"imagen_{i}")
        url = get(f"imagen_{i}_url") or getattr(imagen, "url", None)
        if url:
            contenido.append(f"![Imagen {i}]({url})")

    ruta_completa.write_text("\n".join(filter(None, contenido)), encoding="utf-8")
    return ruta_completa
