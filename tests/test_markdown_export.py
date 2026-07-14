from core.markdown_export import exportar_a_markdown


def test_export_desde_dict(tmp_path):
    log = {
        "fecha_creacion": "2025-08-21T10:00:00Z",
        "nombre_tarea": "Mi tarea",
        "horas": "2.5",
        "tecnologias_utilizadas": "Django",
        "descripcion": "desc",
        "link_respositorio": "https://repo",
        "imagen_1_url": "http://x/img.png",
    }
    ruta = exportar_a_markdown(log, tmp_path)
    texto = ruta.read_text(encoding="utf-8")
    assert ruta.exists()
    assert "# Mi tarea" in texto
    assert "[Repositorio](https://repo)" in texto
    # Regresión: la imagen debe salir cuando el origen es un dict (imagen_i_url).
    assert "![Imagen 1](http://x/img.png)" in texto


def test_nombre_archivo_sanitizado(tmp_path):
    """Regresión de seguridad: el nombre de tarea no debe permitir path traversal."""
    log = {
        "fecha_creacion": "2025-08-21",
        "nombre_tarea": "../../evil name",
        "horas": "1",
        "tecnologias_utilizadas": "",
    }
    ruta = exportar_a_markdown(log, tmp_path)
    assert ruta.parent == tmp_path
    assert ".." not in ruta.name
