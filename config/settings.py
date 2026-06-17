import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-only-for-dev')
# If you are testing locally, set DEBUG to True in your .env file
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
    'broadcast',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Handles static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# --- MEDIA CONFIGURATION ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- STATIC CONFIGURATION ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# FIX: Only look for static files if the directory exists to prevent errors
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# WhiteNoise for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
                'django.template.context_processors.media', 
            ],
        },
    },
]

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}