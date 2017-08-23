import os

DEBUG=True
TEMPLATE_PATH = '%s/templates/' % os.path.dirname(os.path.realpath(__file__))

STATIC_BUCKET = 'nytint-stg-newsapps'
REMOTE_STORAGE_PATH = 'apps/screenshotter'