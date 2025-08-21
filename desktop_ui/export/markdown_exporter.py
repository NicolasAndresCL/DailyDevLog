from datetime import datetime

def exportar_a_markdown(log, ruta_destino):
    fecha = log.fecha_creacion.strftime("%Y-%m-%d")
    nombre_archivo = f"{fecha}_{log.nombre_tarea.replace(' ', '_')}.md"
    ruta_completa = ruta_destino / nombre_archivo

    contenido = f"""# {log.nombre_tarea}

**Fecha:** {fecha}  
**Horas trabajadas:** {log.horas}  
**Tecnologías utilizadas:** {log.tecnologias_utilizadas}

---

## Descripción

{log.descripcion}

---

## Links técnicos

- [Publicación en LinkedIn]({log.link_publicacion_linkedin})
- [IA principal]({log.link_ia_principal})
- [IA secundaria]({log.link_ia_secundaria})
- [IA terciaria]({log.link_ia_terciaria})
- [Repositorio]({log.link_respositorio})
- Commit: `{log.commit_principal}`

---

## Imágenes

"""
    for i in range(1, 4):
        imagen = getattr(log, f"imagen_{i}")
        if imagen:
            contenido += f"![Imagen {i}]({imagen.url})\n"

    with open(ruta_completa, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta_completa
