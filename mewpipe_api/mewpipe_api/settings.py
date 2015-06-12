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
  'social.apps.django_app.default',

  'rest_framework',
  'rest_framework.authtoken',

  #Us
  'rest_api',
)

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
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
  'social.backends.facebook.FacebookOAuth2',
  'social.backends.facebook.FacebookAppOAuth2',
  'social.backends.facebook.Facebook2OAuth2',
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

SOCIAL_AUTH_PIPELINE = (
  'rest_api.social.first_function',

  # Get the information we can about the user and return it in a simple
  # format to create the user instance later. On some cases the details are
  # already part of the auth response from the provider, but sometimes this
  # could hit a provider API.
  'social.pipeline.social_auth.social_details',

  # Get the social uid from whichever service we're authing thru. The uid is
  # the unique identifier of the given user in the provider.
  'social.pipeline.social_auth.social_uid',

  # Checks if the current social-account is already associated in the site.
  'social.pipeline.social_auth.social_user',

  # Make up a username for this person, appends a random string at the end if
  # there's any collision.
  'social.pipeline.user.get_username',

  # Send a validation email to the user to verify its email address.
  # Disabled by default.
  # 'social.pipeline.mail.mail_validation',

  # Associates the current social details with another user account with
  # a similar email address. Disabled by default.
  'social.pipeline.social_auth.associate_by_email',

  # Create a user account if we haven't found one yet.
  'social.pipeline.user.create_user',
  #'rest_api.social.create_user',

  # Create the record that associated the social account with this user.
  'social.pipeline.social_auth.associate_user',

  # Populate the extra_data field in the social record with the values
  # specified by settings (and the default ones like access_token, etc).
  'social.pipeline.social_auth.load_extra_data',

  # Update the user record with any changed info from the auth service.
  'social.pipeline.user.user_details'
  #'rest_api.social.generate_jwt',
)

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
SOCIAL_AUTH_USER_MODEL = "rest_api.UserAccount"

#Used to redirect the user once the auth process ended successfully. The value of ?next=/foo is used if it was present
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
#URL where the user will be redirected in case of an error
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
#Is used as a fallback for LOGIN_ERROR_URL
SOCIAL_AUTH_LOGIN_URL = '/'
#Used to redirect new registered users, will be used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL if defined.
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
#Like SOCIAL_AUTH_NEW_USER_REDIRECT_URL but for new associated accounts (user is already logged in). Used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/'
#The user will be redirected to this URL when a social account is disconnected
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'
#Inactive users can be redirected to this URL when trying to authenticate. 
SOCIAL_AUTH_INACTIVE_USER_URL = '/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGIN_ERROR_URL    = '/'