import os
import sys
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-only-for-dev')

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['scmm-center-broadcast-website-production.up.railway.app', 'localhost', '127.0.0.1', '*']

CSRF_TRUSTED_ORIGINS = ['https://scmm-center-broadcast-website-production.up.railway.app']

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

# Robust Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    try:
        DATABASES = {'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)}
    except Exception:
        DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# Cloudinary Configuration
cloudinary_name = os.getenv('CLOUDINARY_CLOUD_NAME')
cloudinary_key = os.getenv('CLOUDINARY_API_KEY')
cloudinary_secret = os.getenv('CLOUDINARY_API_SECRET')

is_collectstatic = any(arg == 'collectstatic' for arg in sys.argv)
if not is_collectstatic and not DEBUG and not all([cloudinary_name, cloudinary_key, cloudinary_secret]):
    raise ImproperlyConfigured("Cloudinary credentials are missing.")

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': cloudinary_name,
    'API_KEY': cloudinary_key,
    'API_SECRET': cloudinary_secret,
}

# LEGACY STORAGE CONFIGURATION (Required for version 0.3.0)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = ''
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'