import datetime
import importlib
import os
import re
import time

import contextlib
from google.cloud import storage
import selenium.webdriver as webdriver
from urllib.parse import urlencode

def get_env():
    return os.environ.get('DEPLOYMENT_ENVIRONMENT', 'dev')

settings = importlib.import_module('config.%s.settings' % get_env())

def valid_uuid(possible_uuid):
    """
    Checks that a possible UUID4 string is a valid UUID4.
    """
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(possible_uuid)
    return bool(match)

def clean_payload(payload):
    """
    Serializes a payload from form strings to more useful Python types.
    `payload` is a dictionary where both keys and values are exclusively strings.
    * empty string becomes None
    * applies a true / false test to possible true / false string values.
    """
    output = {}
    for k,v in payload.items():

        # Takes the first value.
        v = v[0]

        # Serializes values
        if v == u'':
            v = None
        if v.lower() in ['true', 'yes', 'y', '1']:
            v = True
        if v.lower() in ['false', 'no', 'n', '0']:
            v = False

        # Values not in the test pass through.
        output[k] = v
    return output

def persist_file(path):
    client = storage.Client()
    bucket = client.get_bucket(settings.STATIC_BUCKET)
    local_filename = path.split('/')[-1]
    remote_path = '%s/%s' % (settings.REMOTE_STORAGE_PATH, local_filename)
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(filename=path)
    blob.make_public()
    return blob.public_url.replace('apps%2Fscreenshotter%2F', 'apps/screenshotter/')

def generate_filename(url):
    timestamp = str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0]
    return "%s-%s" % (urlencode({"url": url}).split('url=')[1], timestamp)

@contextlib.contextmanager
def quitting(thing):
    yield thing
    thing.quit()

def screenshot(url, base_output_path=None):
    if not base_output_path:
        base_output_path = "/tmp"
    output_path = "%s/%s.png" % (base_output_path, generate_filename(url))

    with quitting(webdriver.Chrome()) as driver:
        driver.implicitly_wait(10)
        driver.get(url)
        driver.get_screenshot_as_file(output_path)
    
    public_url = persist_file(output_path)

    return public_url