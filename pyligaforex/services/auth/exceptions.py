from pycloudia.cluster.resolver import ResolverMeta, resolve_method

from pyligaforex.services.auth.consts import VERBOSE


class AuthenticationFailed(RuntimeError):
    pass


class Resolver(object):
    __metaclass__ = ResolverMeta

    EMPTY = {}

    @resolve_method(AuthenticationFailed, verbose=VERBOSE.AUTHENTICATION_FAILED)
    def on_authentication_failed(self, exception):
        return self.EMPTY
