import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-only-for-dev')

DEBUG = False

# Updated ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS for Railway
ALLOWED_HOSTS = ['scmm-center-broadcast-website-production.up.railway.app']

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

# --- SECURITY SETTINGS ---
# Railway handles SSL termination, so we keep these True but ensure 
# SECURE_SSL_REDIRECT is handled correctly by the infrastructure
SECURE_SSL_REDIRECT = False 
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Added for proxy reliability
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'config.urls'

# ... [Keep your TEMPLATES configuration exactly as it is] ...

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ... [Keep your LANGUAGE_CODE and TIME_ZONE settings] ...

# --- STATIC AND MEDIA SETTINGS ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'