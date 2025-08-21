# DailyDevLog

**DailyDevLog** es una aplicación multiplataforma para registrar avances técnicos diarios, con trazabilidad visual, exportación a Markdown, autenticación JWT y arquitectura reproducible. Combina backend Django REST con una GUI en PySide6, integrando imágenes, links técnicos y branding profesional.

---

### Tecnologías principales

| Componente         | Tecnología / Framework                         | Propósito                                                                 |
|--------------------|--------------------------------------------------|---------------------------------------------------------------------------|
| Backend API        | Django + Django REST Framework                  | Registro de tareas, autenticación, exportación                           |
| Autenticación      | djangorestframework-simplejwt                   | Login seguro con JWT                                                     |
| Documentación API  | drf-spectacular + Swagger UI                    | Documentación automática y visual                                        |
| Base de datos      | MySQL + SQLAlchemy + Alembic                    | Persistencia, migraciones controladas                                    |
| GUI escritorio     | PySide6 + QtCharts                              | Interfaz visual para registrar, visualizar y exportar tareas             |
| Exportación        | Markdown + Pillow                               | Exportación técnica con previews de imágenes                             |
| Testing            | Pytest + SQLite en memoria                      | Pruebas reproducibles y aisladas                                         |
| Empaquetado        | PyInstaller                                     | Generación de ejecutable multiplataforma                                 |
| DevOps             | git filter-repo + githooks + .env por rama      | Seguridad, trazabilidad y automatización                                 |
| Documentación      | MkDocs + mkdocs-material                        | Showcase técnico y branding internacional                                |

---

### Estructura del proyecto

DailyDevLog/
config/ # settings, urls, wsgi
desktop_ui/ # modelos, serializers, views, GUI
models.py
serializers.py
views/
export/ # markdown_exporter.py
main.py # entrada GUI
media/ # imágenes adjuntas
templates/ # (opcional) vistas HTML
requirements.txt
manage.py
README.md
DailyDevLog/ ├── config/ # settings, urls, wsgi ├── desktop_ui/ # modelos, serializers, views, GUI │ ├── models.py │ ├── serializers.py │ ├── views/ │ ├── export/ # markdown_exporter.py │ └── main.py # entrada GUI ├── media/ # imágenes adjuntas ├── templates/ # (opcional) vistas HTML ├── requirements.txt ├── manage.py └── README.md

Código

---

### Autenticación JWT

- Endpoint de login: `POST /api/token/`
- Endpoint de refresh: `POST /api/token/refresh/`
- Protegido con `IsAuthenticated` en vistas sensibles

---

### Testing reproducible

- Base de datos SQLite en memoria
- Fixtures modulares
- Cobertura con `pytest-cov`
- Aislamiento total por entorno

---

### Exportación a Markdown

Cada tarea registrada puede exportarse como archivo `.md` con:

- Nombre, fecha, horas, tecnologías
- Descripción técnica
- Links a publicaciones, IA, repositorio y commit
- Previews de imágenes adjuntas

---

### Branding técnico

- Documentación bilingüe
- Showcase con changelogs diarios
- Integración con LinkedIn y portafolio
- Automatización de backups y exportaciones

---

### Setup rápido

```bash
git clone https://github.com/tuusuario/DailyDevLog.git
cd DailyDevLog
python -m venv env
source env/bin/activate  # o env\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### 📌 Autor
Nicolás Andrés Cano Leal Backend & Frontend Developer | Django REST | PySide6 | DevOps 📍 Rancagua, Chile | Visa vigente para EE.UU. 🔗 LinkedIn | Portafolio
