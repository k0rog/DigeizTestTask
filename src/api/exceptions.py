from flask import jsonify, make_response


class AppException(Exception):
    """Base exception to be caught"""

    http_code = 400

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class AlreadyExistsException(AppException):
    """Duplicate PK"""


class ValidationException(AppException):
    """Domain constraint violation"""


class DoesNotExistException(AppException):
    """Domain constraint violation"""

    http_code = 404


class AccessDeniedException(AppException):
    """Attempt to modify constant data"""


def app_exception_handler(exception):
    http_code = exception.http_code
    r = make_response({'error': str(exception)}, http_code)
    return r


def api_exception_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request.'])
    if headers:
        return jsonify({'errors': messages}), err.code, headers
    else:
        return jsonify({'errors': messages}), err.code
