from pycloudia.uitls.defer import inline_callbacks, deferrable

from im.services.facades.exceptions import ClientNotFoundError
from im.services.gateways.consts import HEADER
from im.services.gateways.interfaces import IRunner, IRunnerFactory


class Runner(IRunner):
    """
    :type dao: L{im.services.gateways.interfaces.IDao}
    :type router: L{im.services.gateways.interfaces.IRouter}
    :type clients: L{im.services.facades.interfaces.IService}
    """
    dao = None
    router = None
    clients = None

    def __init__(self, client_id):
        self.client_id = client_id
        self.client_address = None
        self.client_user_id = None

    @inline_callbacks
    def set_client_address(self, address):
        self.client_address = yield self.dao.set_gateway_client_address(self.client_id, address)

    @inline_callbacks
    def set_client_user_id(self, user_id):
        self.client_user_id = yield self.dao.set_gateway_client_user_id(self.client_id, user_id)

    @inline_callbacks
    def process_incoming_package(self, package):
        package = self._drop_internal_headers(package)
        package.headers[HEADER.INTERNAL.USER_ID] = self.client_user_id
        package.headers[HEADER.INTERNAL.CLIENT_ID] = self.client_id
        response_package = yield self.router.route_package(package)
        if response_package is not None:
            self.process_outgoing_package(response_package)

    @deferrable
    def process_outgoing_package(self, package):
        package = self._drop_internal_headers(package)
        self.clients.process_outgoing_package(self.client_address, self.client_id, package)

    @staticmethod
    def _drop_internal_headers(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        for header_name in package.headers.keys():
            if header_name.startswith(HEADER.INTERNAL_PREFIX):
                del package.headers[header_name]
        return package


class RunnerFactory(IRunnerFactory):
    """
    :type dao: L{im.services.gateways.interfaces.IDao}
    :type router: L{pycloudia.cluster.interfaces.ISender}
    :type facades: L{im.services.facades.interfaces.IService}
    """
    dao = None
    router = None
    facades = None

    def __call__(self, client_id):
        instance = Runner(client_id)
        instance.dao = self.dao
        instance.router = self.router
        instance.clients = self.facades
        return instance
