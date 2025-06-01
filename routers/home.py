# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from common.errors import APIError

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/200', methods=['GET'])
def hello():
    raise APIError(status_code=200, message='Hello World')

@home_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
