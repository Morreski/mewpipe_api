

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

PAGINATION_LIMIT = 100
VIDEO_PAGINATION_LIMIT = 25

VIEW_TIMEOUT = 60 #minutes, Decide interval between two view incrementation
VIEW_TTL = 24 #hours, View time to live

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mewpipe',
        'USER' : 'mewpipe',
        'PASSWORD' : 'HELmhwn6aRd3WB79',
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}
