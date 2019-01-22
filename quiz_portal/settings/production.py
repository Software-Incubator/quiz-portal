from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}

STATIC_ROOT = os.path.join('/home/si', 'Assets/QuizPortal/static')

MEDIA_ROOT = os.path.join('/home/si', "Assets/QuizPortal/media")
