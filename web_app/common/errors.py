# -*- coding: utf-8 -*-

class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=200, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

