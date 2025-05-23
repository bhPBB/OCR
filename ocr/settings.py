from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environ
env = environ.Env(DEBUG=(bool, False), LOCAL=(bool, True))
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env("DEBUG")

LOCAL = env("LOCAL")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

if not LOCAL:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['localhost'])
    CSRF_TRUSTED_ORIGINS = env.list('CSRF', default=['https://localhost:8000'])
    CSRF_ALLOWED_ORIGINS = env.list('CSRF', default=['https://localhost:8000'])
    CORS_ORIGINS_WHITELIST = env.list('CSRF', default=['https://localhost:8000'])
else:
    # Local
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    CSRF_TRUSTED_ORIGINS = ['https://localhost:8000', 'https://127.0.0.1:8000']
    CSRF_ALLOWED_ORIGINS = ['https://localhost:8000', 'https://127.0.0.1:8000']
    CORS_ORIGINS_WHITELIST = ['https://localhost:8000', 'https://127.0.0.1:8000']

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'recibos_arquivamento',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ocr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ocr.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

BUCKET = env("BUCKET")

if LOCAL:
    # Local
    STATIC_ROOT = BASE_DIR / 'static'
    STATIC_URL = "static/"
else:
    # App Engine
    STATIC_URL = f'https://storage.googleapis.com/{BUCKET}/'

MEDIA_URL = f'https://storage.googleapis.com/{BUCKET}/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-storages
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': BUCKET,
            'project_id': env('GS_PROJECT_ID'),
            'default_acl': env('GS_DEFAULT_ACL'),
            'location': 'media/'
        }
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': BUCKET,
            'project_id': env('GS_PROJECT_ID'),
            'default_acl': env('GS_DEFAULT_ACL'),
            'location': 'static/' 
        }
    }
}