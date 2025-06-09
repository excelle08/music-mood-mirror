# -*- coding: utf-8 -*-

# routers/error_maker.py
from flask import Blueprint
from werkzeug.exceptions import default_exceptions

from common.errors import APIError

error_blueprint = Blueprint('error_maker', __name__)

@error_blueprint.route('/error/<int:code>', methods=['GET'])
def make_error(code):
    if code not in default_exceptions:
        raise APIError(status_code=404, message='Not an HTTP status code for error')
    raise default_exceptions[code]
