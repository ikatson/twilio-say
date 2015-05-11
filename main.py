#!/usr/bin/env python

import logging
import os

from flask import Flask, abort, request

import twilio.twiml
from twilio.util import RequestValidator

app = Flask(__name__)

TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_TOKEN = os.environ['TWILIO_TOKEN']
TWILIO_DEFAULT_SAY = os.environ['TWILIO_DEFAULT_SAY']
DEBUG = os.environ.get('DEBUG', False)

logger = logging.getLogger('twilio-sayer')

def get_original_request_url(request):
    # request.url does not exactly equal the opened URL,
    # because the query string gets unescaped in some places.
    url = request.url.split('?')[0]
    qs = request.environ.get('QUERY_STRING', '')
    if qs:
        url = '%s?%s' % (url, qs)
    return url


@app.route("/", methods=['GET', 'POST'])
def answer():
    validator = RequestValidator(TWILIO_TOKEN)
    signature = request.headers.get('X-Twilio-Signature', '')
    url = get_original_request_url(request)
    logger.info('Got request: url: %r, post: %r, signature: %r',
                url, dict(request.form.iteritems()), signature)
    if not validator.validate(url, request.form, signature):
        return abort(403)

    say = request.args.get('say', TWILIO_DEFAULT_SAY)
    resp = twilio.twiml.Response()

    # If there is no pause, you might not hear the beginning of the message.
    resp.pause(length=2)
    resp.say(say)

    # Repeat the message in case the receiver missed it.
    resp.pause(length=5)
    resp.say(say)

    return str(resp)

def setup_logging(app):
    root_logger = logging.getLogger()
    if DEBUG:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)


def set_debug(app):
    app.debug = bool(DEBUG)

setup_logging(app)
set_debug(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
