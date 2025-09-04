import environ
import os
from pathlib import Path
from datetime import timedelta

# Inicializar entorno
env = environ.Env(
    DEBUG=(bool, False)
)

# Cargar archivo .env.dev
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env.dev'))

BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'rest_framework',
    'desktop_ui',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # tu frontend local
]


# URLs y WSGI
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Base de datos
DATABASES = {
    'default': env.db(),  # Ej: sqlite:///db.sqlite3 o mysql://user:pass@host/db
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = env('TIME_ZONE', default='UTC')
USE_I18N = True
USE_TZ = True

# Archivos estáticos y multimedia
STATIC_URL = 'static/'
MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / env('MEDIA_ROOT', default='media')

# Configuración por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF y JWT
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DailyDevLog API',
    'DESCRIPTION': 'Registro técnico diario de tareas TI con trazabilidad y documentación automática.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'displayOperationId': True,
        'filter': True,
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
