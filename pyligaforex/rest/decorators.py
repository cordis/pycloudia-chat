from functools import wraps

try:
    import simplejson as json
except ImportError:
    import json

from tornado.web import HTTPError, RequestHandler

from pycloudia.uitls.decorators import generate_list, generate_dict
from pycloudia.uitls.defer import maybe_deferred, return_value, inline_callbacks


def http_request_handler(cls):
    @wraps(cls)
    class RequestHandlerDecorator(RequestHandler):
        subject = None

        def prepare(self):
            self.subject = cls()

        def get(self, *args, **kwargs):
            deferred = maybe_deferred(self.subject.get(*args, **kwargs))
            deferred.addCallbacks(self._send_success, self._send_failure)

        def _send_success(self, response):
            self.finish(json.dumps({
                'data': response,
                'code': 0,
                'message': None,
            }))

        def _send_failure(self, exception):
            self.finish(json.dumps({
                'data': None,
                'code': self._get_failure_code(exception),
                'message': str(exception),
            }))

        @staticmethod
        def _get_failure_code(exception):
            if isinstance(exception, HTTPError):
                return exception.status_code
            return getattr(exception, 'code', 500)

    return RequestHandlerDecorator


def http_error(exception_cls, code):
    def http_error_call(func):
        @wraps(func)
        def http_error_decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_cls as e:
                raise HTTPError(code, e)
        return http_error_decorator
    return http_error_call


def http_jsonify(encode_func):
    def http_jsonify_call(func):
        @wraps(func)
        @inline_callbacks
        def http_jsonify_decorator(*args, **kwargs):
            obj = yield maybe_deferred(func(*args, **kwargs))
            return_value(encode_func(obj))
        return http_jsonify_decorator
    
    return http_jsonify_call


def http_jsonify_list(encode_func):
    @generate_list
    def encode_list(obj_list):
        for obj in obj_list:
            yield encode_func(obj)

    def http_jsonify_list_call(func):
        @wraps(func)
        @inline_callbacks
        def http_jsonify_list_decorator(*args, **kwargs):
            obj_list = yield maybe_deferred(func(*args, **kwargs))
            return_value(encode_list(obj_list))
        return http_jsonify_list_decorator

    return http_jsonify_list_call


def http_jsonify_dict(encode_func):
    @generate_dict
    def encode_dict(obj_dict):
        for key, obj in obj_dict.iteritems():
            yield key, encode_func(obj)

    def http_jsonify_dict_call(func):
        @wraps(func)
        @inline_callbacks
        def http_jsonify_dict_decorator(*args, **kwargs):
            obj_dict = yield maybe_deferred(func(*args, **kwargs))
            return_value(encode_dict(obj_dict))
        return http_jsonify_dict_decorator

    return http_jsonify_dict_call
