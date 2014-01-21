from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.cluster.beans import Activity

from im.services.facades.exceptions import ClientNotFoundError
from im.services.gateways.consts import HEADER, DEFAULT, SERVICE
from im.services.gateways.interfaces import IRunner, IRunnerFactory
from im.services.gateways.exceptions import HeaderNotFoundError


class Runner(IRunner):
    """
    :type dao: L{im.services.gateways.interfaces.IDao}
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type facades: L{im.services.facades.interfaces.IService}
    """
    dao = None
    sender = None
    facades = None

    def __init__(self, client_id):
        self.client_id = client_id
        self.facade_address = None
        self.user_id = None
        self.activity = Activity(service=SERVICE.NAME, runtime=self.client_id)

    def get_activity(self):
        return self.activity

    @inline_callbacks
    def set_facade_address(self, facade_address):
        self.facade_address = yield self.dao.set_gateway_facade_address(self.client_id, facade_address)

    @inline_callbacks
    def set_user_id(self, user_id):
        self.user_id = yield self.dao.set_gateway_user_id(self.client_id, user_id)

    @deferrable
    def process_outgoing_package(self, package):
        package = self._drop_internal_headers(package)
        self.facades.process_outgoing_package(self.facade_address, self.client_id, package)

    @inline_callbacks
    def process_incoming_package(self, package):
        target = self._pop_external_target(package)
        package = self._drop_internal_headers(package)
        package = self._copy_external_command(package)
        package.headers[HEADER.INTERNAL.USER_ID] = self.user_id
        package.headers[HEADER.INTERNAL.CLIENT_ID] = self.client_id
        response_package = yield self._route_package(target, package)
        if response_package is not None:
            self.process_outgoing_package(response_package)

    @staticmethod
    def _pop_external_target(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: C{pycloudia.cluster.beans.Activity}
        :raise: L{im.services.gateways.exceptions.HeaderNotFoundError}
        """
        try:
            service = package.headers.pop(HEADER.EXTERNAL.SERVICE)
        except KeyError:
            raise HeaderNotFoundError(HEADER.EXTERNAL.SERVICE)
        else:
            runtime = package.headers.pop(HEADER.EXTERNAL.RUNTIME, hash(package))
            #@TODO: consider runtime = package.headers.pop(HEADER.EXTERNAL.RUNTIME, hash(self.client_id))
            return Activity(service=service, runtime=runtime)

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

    @staticmethod
    def _copy_external_command(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        :raise: L{im.services.gateways.exceptions.HeaderNotFoundError}
        """
        try:
            package.headers[HEADER.INTERNAL.COMMAND] = package.headers.pop(HEADER.EXTERNAL.COMMAND)
        except KeyError:
            raise HeaderNotFoundError(HEADER.EXTERNAL.COMMAND)
        else:
            return package

    @deferrable
    def _route_package(self, target, package):
        """
        :type target: L{pycloudia.cluster.beans.Activity}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage} or C{None}
        """
        try:
            request_id = package.headers.pop(HEADER.EXTERNAL.REQUEST_ID)
        except KeyError:
            return self._send_package(target, package)
        else:
            return self._send_request_package(request_id, target, package)

    @inline_callbacks
    def _send_request_package(self, request_id, target, request_package):
        """
        :type request_id: C{str}
        :type target: L{pycloudia.cluster.beans.Activity}
        :type request_package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage}
        """
        timeout = self._get_external_timeout(request_package)
        response_package = yield self.sender.send_request_package(self.activity, target, request_package, timeout)
        response_package.headers[HEADER.EXTERNAL.RESPONSE_ID] = request_id
        return_value(response_package)

    @staticmethod
    def _get_external_timeout(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: C{int}
        """
        try:
            return package.headers.pop(HEADER.EXTERNAL.TIMEOUT)
        except KeyError:
            return DEFAULT.EXTERNAL.TIMEOUT

    def _send_package(self, target, package):
        """
        :type target: L{pycloudia.cluster.beans.Activity}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
        self.sender.send_package(target, package)


class RunnerFactory(IRunnerFactory):
    """
    :type dao: L{im.services.gateways.interfaces.IDao}
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type facades: L{im.services.facades.interfaces.IService}
    """
    dao = None
    sender = None
    facades = None

    def __call__(self, client_id):
        instance = Runner(client_id)
        instance.dao = self.dao
        instance.sender = self.sender
        instance.facades = self.facades
        return instance
