# DailyDevLog
DailyDevLog es una aplicación multiplataforma para registrar avances técnicos diarios, con trazabilidad visual, exportación a Markdown, autenticación JWT y arquitectura reproducible. Combina backend Django REST con una GUI en PySide6 y un frontend moderno en React + Radix UI, integrando imágenes, links técnicos y branding profesional.

## Tecnologías principales

| Componente | Tecnología / Framework | Propósito |
| --- | --- | --- |
| Backend API | Django + Django REST Framework | Registro de tareas, autenticación, exportación |
| Autenticación | djangorestframework-simplejwt | Login seguro con JWT |
| Documentación API | drf-spectacular + Swagger UI | Documentación automática y visual con esquema JWT |
| Frontend web | React + Radix UI + Stitches | Interfaz moderna, accesible y coherente con tema oscuro tipo VSCode |
| Base de datos | SQLite (dev) + MySQL (prod) | Persistencia local y escalable |
| GUI escritorio | PySide6 + QtCharts | Interfaz visual para registrar, visualizar y exportar tareas |
| Exportación | Markdown + Pillow | Exportación técnica con previews de imágenes |
| Testing | Pytest + SQLite en memoria | Pruebas reproducibles y aisladas |
| Empaquetado | PyInstaller | Generación de ejecutable multiplataforma |
| DevOps | git filter-repo + githooks + .env por rama | Seguridad, trazabilidad y automatización |
| Documentación | MkDocs + mkdocs-material | Showcase técnico y branding internacional |

## Estructura del proyecto

* Código
	+ DailyDevLog/
		- config/                  # settings, urls, wsgi
		- desktop_ui/             # modelos, serializers, views, GUI
			- models.py
			- serializers.py
			- views/
			- export/             # markdown_exporter.py
			- main.py             # entrada GUI
		- media/                  # imágenes adjuntas
		- templates/              # (opcional) vistas HTML
		- requirements.txt
		- manage.py
		- README.md

## Autenticación JWT

* Endpoint de login: POST /api/token/
* Endpoint de refresh: POST /api/token/refresh/
* Documentado en Swagger con auth: Bearer
* Protegido con IsAuthenticated en POST, PUT, PATCH, DELETE
* Solo usuarios autenticados pueden registrar tareas

## Documentación Swagger

* Integración completa con drf-spectacular
* Decoración de vistas con extend_schema_view y auth: Bearer
* Separación por tags: DailyLog, Autenticación
* Visualización clara de endpoints protegidos y públicos

## Refactorizaciones recientes

* Protección granular de endpoints sensibles con JWT
* Separación de permisos por método (get público, post privado)
* Eliminación de previews de imágenes en GUI por limitaciones técnicas
* Refactor visual completo con tema oscuro tipo VSCode
* Validación visual en frontend si el token es inválido o falta
* Login funcional con persistencia de token y logout controlado
* Exportación Markdown con estructura técnica y branding

## Frontend React

* Login con JWT y persistencia en localStorage
* Envío de token en headers Authorization: Bearer
* Mensajes visuales si el usuario no está autenticado
* Tabs modulares: Formulario, Historial, Estadísticas
* Estilo accesible y coherente con Radix UI + Stitches

## Testing reproducible

* Base de datos SQLite en memoria
* Fixtures modulares
* Cobertura con pytest-cov
* Aislamiento total por entorno

## Exportación a Markdown

* Cada tarea registrada puede exportarse como archivo .md con:
	+ Nombre, fecha, horas, tecnologías
	+ Descripción técnica
	+ Links a publicaciones, IA, repositorio y commit
	+ Previews de imágenes adjuntas (si están disponibles)

## Branding técnico

* Documentación bilingüe
* Showcase con changelogs diarios
* Integración con LinkedIn y portafolio
* Automatización de backups y exportaciones

## Setup rápido

bash
git clone https://github.com/NicolasAndresCL/DailyDevLog.git
cd DailyDevLog
python -m venv env
source env/bin/activate  # o env\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Autor

Nicolás Andrés Cano Leal
Backend & Frontend Developer | Django REST | PySide6 | React | DevOps
Rancagua, Chile | Visa vigente para EE.UU.
[LinkedIn](https://www.linkedin.com/in/nicolasandrescl/) | [Portafolio](https://nicolasandrescl.github.io/)
