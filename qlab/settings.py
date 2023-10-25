"""
Django settings for qlab project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta

from corsheaders.defaults import default_headers

from pathlib import Path
from environ import Env


BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(BASE_DIR / '.env')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

DEVELOPMENT_MODE = env.bool('DEVELOPMENT_MODE', False)

# Keeps system safe from abusing, may need to False on development mode
ATTEMPT_PROTECTION = env.bool('ATTEMPT_PROTECTION', True)


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

SHARED_APPS = [
    'django_tenants',
    'qlab.apps.tenant',
    'django.contrib.contenttypes',
    'qlab.apps.accounts',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'rest_framework.authtoken',
    'qlab.apps.core',
    'qlab.apps.company',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'drf_yasg',
]

TENANT_APPS = [
    'django.contrib.contenttypes',
    'qlab.apps.accounts',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'rest_framework.authtoken',
    'qlab.apps.core',
    'qlab.apps.company',
]

INSTALLED_APPS = SHARED_APPS + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

AUTH_USER_MODEL = 'accounts.User'

TENANT_MODEL = 'tenant.Organization'

TENANT_DOMAIN_MODEL = 'tenant.Domain'
TENANT_SUBFOLDER_PREFIX = 'organization'

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django_tenants.middleware.TenantSubfolderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'qlab.apps.core.middleware.TenantMediaMiddleware'
]

ROOT_URLCONF = 'qlab.urls'

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

WSGI_APPLICATION = 'qlab.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': env.str('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST', 'localhost'),
        'PORT': env.str('DB_PORT', '5432'),
    }
}

DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)

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


LANGUAGE_CODE = 'tr-tr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


STATIC_ROOT = '/app/qlab/static/'

DEFAULT_FILE_STORAGE = 'django_tenants.files.storage.TenantFileSystemStorage'
MULTITENANT_RELATIVE_MEDIA_ROOT = ''

MEDIA_ROOT = '/app/qlab/media/'
MEDIA_URL = 'media/'
MEDIA_DOMAIN = env.str('MEDIA_DOMAIN')
TENANT_STORAGE_FOLDER = 'tenant_storage'


SEND_SMS = env.bool('SEND_SMS')
SEND_EMAIL = env.bool('SEND_EMAIL')
EMAIL_USE_TLS = True
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = (*default_headers, 'org', 'branch')
