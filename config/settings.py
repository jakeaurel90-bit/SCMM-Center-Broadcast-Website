import os
import sys
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-only-for-dev')

# Dynamic DEBUG and ALLOWED_HOSTS
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['scmm-center-broadcast-website-production.up.railway.app', 'localhost', '127.0.0.1', '*']

CSRF_TRUSTED_ORIGINS = [
    'https://scmm-center-broadcast-website-production.up.railway.app',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'broadcast',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Cloudinary Configuration with Build-Time Safety
cloudinary_name = os.getenv('CLOUDINARY_CLOUD_NAME')
cloudinary_key = os.getenv('CLOUDINARY_API_KEY')
cloudinary_secret = os.getenv('CLOUDINARY_API_SECRET')

# We skip the check if we are running 'collectstatic' so the build succeeds
is_collectstatic = any(arg == 'collectstatic' for arg in sys.argv)

if not is_collectstatic and not all([cloudinary_name, cloudinary_key, cloudinary_secret]):
    raise ImproperlyConfigured("Cloudinary credentials are missing from environment variables.")

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': cloudinary_name,
    'API_KEY': cloudinary_key,
    'API_SECRET': cloudinary_secret,
}

# MODERN STORAGE CONFIGURATION (Fixes the AttributeError)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'