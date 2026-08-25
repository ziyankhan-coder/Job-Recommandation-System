from pathlib import Path
import os
import environ
import dj_database_url
# Django ka default BASE_DIR pehle se bana hoga, ise wahi rehne do:
BASE_DIR = Path(__file__).resolve().parent.parent

# Ab hamara env initialization aur path read logic
env = environ.Env()

# '..' lagane se Django jobrecommendation folder se bahar nikal kar 
# main root folder ke .env file ko sahi se read kar payega!
environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))
# ... baaki ka saara code iske niche chalta rahega ...

# Ab settings.py mein jahan SECRET_KEY hai, use bhi safe kar lo:
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key')
DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'job',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Yeh line yahan add karo
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # <-- CORS Middleware yahan aayega
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jobrecommendation.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]

WSGI_APPLICATION = 'jobrecommendation.wsgi.application'

# DATABASES configuration
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_USER_MODEL = 'account.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# React runs on port 5173 by default
# Purana CORS settings hata kar sirf yeh do lines rakhein:
CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = ['*', 'job-recommandation-system-dsv6.onrender.com', 'localhost', '127.0.0.1']
import os
STATIC_URL = '/static/'
# Yeh line ensure karegi ki local development mein Django ko static files milen
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Yeh collectstatic files store karne ke liye hai
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'