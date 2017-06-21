# -*- coding: utf-8 -*-
import os

import coloredlogs
from flask import Flask, send_from_directory
from flask_cors import CORS

from trailblazer.server import api, ext

coloredlogs.install(level='INFO')
app = Flask(__name__, static_folder='static', static_url_path='')

SECRET_KEY = 'unsafe!!!'
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_POOL_RECYCLE = 7200
SQLALCHEMY_TRACK_MODIFICATIONS = 'FLASK_DEBUG' in os.environ
GOOGLE_OAUTH_CLIENT_ID = os.environ['GOOGLE_OAUTH_CLIENT_ID']
GOOGLE_OAUTH_CLIENT_SECRET = os.environ['GOOGLE_OAUTH_CLIENT_SECRET']

app.config.from_object(__name__)

# register blueprints
app.register_blueprint(api.blueprint)

# configure extensions
ext.store.init_app(app)
ext.auth.init_app(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
