# Refactor estructural y validación visual con Celery-DjangoRestFramework
**Fecha:** 2025-08-24
**Horas trabajadas:** 2.00
**Tecnologías utilizadas:** Django, Django Rest Framework, Celery, Redis, PySide6, Pillow, DRF Spectacular, Python, Git
---
## Descripción
Se realizó una refactorización completa del árbol de directorios, consolidando las apps bajo apps/ para mejorar la trazabilidad y modularidad del proyecto. Se creó la app core con estructura para tareas Celery, incluyendo validate.py para verificación de imágenes en productos. Se implementó un endpoint DRF con GenericAPIView y extend_schema_view para disparar la validación visual desde la API. Además, se actualizó la configuración de Celery en config/celery.py y se registraron los cambios en requirements.txt, dejando el proyecto listo para escalar con GUI y exportación profesional.
---
## Links técnicos
- [IA principal](https://copilot.microsoft.com/chats/qFKBDDteg2PvNJa9x6GHV)
- [Repositorio](https://github.com/NicolasAndresCL/API_con_DRF)
- Commit: `Refactor project structure: moved apps to unified namespace, added core tasks and DRF endpoint for image validation, updated Celery config and requirements.`
---
## Imágenes