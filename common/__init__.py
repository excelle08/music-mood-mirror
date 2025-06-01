# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, Response, render_template, jsonify
from werkzeug.exceptions import default_exceptions
from common.errors import APIError
from common.model import db
from config.settings import SQLITE_DB_URI, SECRET_KEY
from routers.error_maker import error_blueprint
from routers.home import home_blueprint
from routers.lyrics_api import lyrics_api
from routers.auth import auth
from routers.history import history


def create_app():
    app = Flask(__name__,
        static_folder=os.path.join(os.path.dirname(__file__), "..", 'static'),
        template_folder=os.path.join(os.path.dirname(__file__), "..", 'templates')
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)

    app.register_blueprint(error_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(lyrics_api)
    app.register_blueprint(auth)
    app.register_blueprint(history)

    register_error_handler(app)

    with app.app_context():
        db.create_all()

    return app


def return_json(serializable):
    return Response(json.dumps(serializable), mimetype='application/json')


def register_error_handler(app):
    # Handle APIError exceptions
    @app.errorhandler(APIError)
    def handle_api_error(error):
        err = {
            'url': 'https://excelle08.me/images/cat/%d.jpg' % error.status_code,
            'message': error.message,
            'code': error.status_code
        }
        content = render_template('error_meow.html', err=err)
        return Response(content, status=error.status_code)
    # Handle HTTP exceptions
    for code in default_exceptions:
        app.errorhandler(code)(handle_http_error)
    # Handle KeyError exceptions
    @app.errorhandler(KeyError)
    def handle_key_error(error):
        response = jsonify(error=200, message='Missing key %s' % str(error.message), data='')
        response.status_code = 200
        return response


def handle_http_error(error):
    code = error.code
    desc = error.description
    return Response(
        render_template('error_meow.html', err={
            'url': 'https://excelle08.me/images/cat/%d.jpg' % error.code,
            'code': code,
            'message': desc
        }),
        status=code
    )


