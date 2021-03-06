from flask import Flask, request, Response, session
from flask_sslify import SSLify

app = Flask(__name__)
app.config.from_object('flask_app.settings')

import flask_app.endpoints
