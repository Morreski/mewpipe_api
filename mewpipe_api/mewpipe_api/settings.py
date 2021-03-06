from .settings_local import *
from .social_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$y(^e0r%yzum0m*$3k4r2tdf4vh3itop8k=c0@3_o7(9_a+4=d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
REST_FRAMEWORK = {
  'DEFAULT_PAGINATION_CLASS': 'rest_api.paginators.BasePaginator',
  'DEFAULT_FILTER_BACKENDS' : ('rest_framework.filters.DjangoFilterBackend',)
}

# Application definition

INSTALLED_APPS = (
  'django.contrib.sites',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  #External Libs
  'django_extensions',
  'djcelery',
  'django_facebook',
  'open_facebook',

  'rest_framework',
  'rest_framework.authtoken',

  #Us
  'rest_api',
)

MIDDLEWARE_CLASSES = (
#  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',

  'rest_api.middlewares.auth.JwtAuth',
  'rest_api.middlewares.crossdomain_middleware.XsSharing',
)

APPEND_SLASH=False

AUTHENTICATION_BACKENDS = (
  'django_facebook.auth_backends.FacebookBackend',
  'django.contrib.auth.backends.ModelBackend',   
)

ROOT_URLCONF = 'mewpipe_api.urls'

TEMPLATE_DIRS = ('templates/', )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mewpipe_api.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# DJANGO ALLAUTH

AUTH_USER_MODEL = "rest_api.UserAccount"