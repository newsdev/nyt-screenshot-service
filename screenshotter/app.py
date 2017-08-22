#!/usr/bin/env python

import argparse
import base64
import csv
import datetime
import glob
import json
import importlib
import io
import os
import re
import time


try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Flask, render_template, request, make_response, Response, redirect, jsonify
import peewee
from peewee import *
from pyiap.pyiap_flask_middleware import VerifyJWTMiddleware

from screenshotter import utils

settings = importlib.import_module('config.%s.settings' % utils.get_env())
app = Flask(__name__)
app.debug=settings.DEBUG

@app.route('/healthcheck', methods=['GET'])
def health():
    return Response('ok')

@app.route('/get/', methods=['POST', 'GET'])
def screenshot():

    if request.method == "POST":
        payload = utils.clean_payload(dict(request.form))

    if request.method == "GET":
        payload = utils.clean_payload(dict(request.args))
    
    url = payload.get('url', None)
    if not url:
        return Response('bad request', 400)

    public_url = utils.screenshot(url)
    r = Response(json.dumps({"screenshot_url": public_url, "url": url}))
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
