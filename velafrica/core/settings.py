"""
Django settings for velafrica_trackingtool project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b2j_&e=rzafa+zo874%tc^h!nbp#%0#442*19@(i&h-&s=v*hh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    # django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom apps
    'daterange_filter',
    'django_resized',
    'simple_history',
    'import_export',
    # custom velafrica apps
    'velafrica.core',
    'velafrica.counter',
    'velafrica.download',
    'velafrica.frontend',
    'velafrica.organisation',
    'velafrica.stock',
    'velafrica.sbbtracking',
    #'velafrica.translation'
    'velafrica.transport',
    'velafrica.velafrica_sud',
    # django storages
    'storages',
)

# Django Storages Settings for SFTP


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'velafrica.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['frontend'],
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

WSGI_APPLICATION = 'velafrica.core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
if 'ON_HEROKU' in os.environ:
    if int(os.environ['ON_HEROKU']) == 1:
        # Parse database configuration from $DATABASE_URL
        import dj_database_url
        DATABASES['default'] =  dj_database_url.config()
        # fasten up database access
        # not working smoothly with free plan 
        # DATABASES['default']['CONN_MAX_AGE'] = 500


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/auth/profile'
LOGOUT_URL = '/auth/logout'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media files (Files uploaded by user)

MEDIA_URL = 'http://partnertool.velafrica.ch/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

# Django Resized
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

# Email settings
EMAIL_HOST = 'smtpauth.creta.ch'
EMAIL_HOST_USER = 'tracking@velafrica.ch'
EMAIL_HOST_PASSWORD = '!0q486ZjXeJilxfmwa#2HOc3PD5n1'
#EMAIL_PORT = 465
#EMAIL_USE_SSL = True

EMAIL_FROM_NAME = 'Velafrica Tracking'
EMAIL_FROM_EMAIL = 'tracking@velafrica.ch'


# Django Storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.ftp.FTPStorage'
FTP_STORAGE_LOCATION = 'ftp://nto5q-partnertoo:B1XqSY78ri0Vb94_hxws-C5nm6co@partnertool.velafrica.ch:21'