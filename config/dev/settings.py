import os

from peewee import *

import screenshotter.utils

DEBUG=True
TEMPLATE_PATH = '%s/templates/' % os.path.dirname(os.path.realpath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'peewee.PostgresqlDatabase',
        'OPTIONS': {
            "database": os.environ.get('DB_NAME', "screenshotter_%s" % utils.get_env()),
            "user": os.environ.get('DB_USER', None),
            "password": os.environ.get('DB_PASSWORD', None),
            "host": os.environ.get('DB_HOST', None),
        }
    }
}

STATIC_BUCKET = 'nytint-stg-newsapps'
REMOTE_STORAGE_PATH = 'apps/screenshotter'