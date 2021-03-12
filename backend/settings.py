from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '93%d5+_^36#3n7i*a=x3gvwi10@1#=9(of=zt#y!o=ld_+p)r*'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates/'
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config()


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Celery application definition
REDIS_URL = config("REDIS_URL")
CELERY_BROKER_URL = config('REDIS_URL')
CELERY_RESULT_BACKEND = config('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


STATICFILES_DIRS = [
    BASE_DIR / "assets",
]

MEDIA_ROOT = BASE_DIR / "media"


AWS_ACCESS_KEY = config('AWS_ACCESS_KEY')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')
AWS_BUCKET_NAME = config('AWS_BUCKET_NAME')
AWS_OUTPUT_BUCKET_NAME = config('AWS_OUTPUT_BUCKET_NAME')
AWS_REGION = config('AWS_REGION')


# Agora Configuration
AGORA_DEFAULT_MERGE_MODE = config('AGORA_DEFAULT_MERGE_MODE', cast=int)
AGORA_DEFAULT_FPS = config('AGORA_DEFAULT_FPS', cast=int)
AGORA_DEFAULT_WIDTH = config('AGORA_DEFAULT_WIDTH', cast=int)
AGORA_DEFAULT_HEIGHT = config('AGORA_DEFAULT_HEIGHT', cast=int)
