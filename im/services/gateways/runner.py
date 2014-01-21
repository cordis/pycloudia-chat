from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.cluster.beans import Activity
from im.services.gateways.interfaces import IRunner
from im.services.gateways.exceptions import HeaderNotFoundError
from im.services.gateways.consts import HEADER, DEFAULT


class Runner(IRunner):
    """
    :type dao: L{im.services.gateways.interfaces.IDao}
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type internal_request_id_factory: C{Callable}
    """
    dao = None
    sender = None
    internal_request_id_factory = None

    def __init__(self, client_id, facade_id, user_id=None):
        self.client_id = client_id
        self.facade_id = facade_id
        self.user_id = user_id

    @deferrable
    def route_package(self, package):
        target = self._get_external_target(package)
        try:
            request_id = package.headers.pop(HEADER.EXTERNAL.REQUEST_ID)
        except KeyError:
            return self._send_package(target, package)
        else:
            return self._send_request_package(target, request_id, package)

    @staticmethod
    def _get_external_target(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: C{pycloudia.cluster.beans.Activity}
        """
        try:
            service = package.headers.pop(HEADER.EXTERNAL.SERVICE)
            runtime = package.headers.pop(HEADER.EXTERNAL.RUNTIME, hash(package))
        except KeyError:
            raise HeaderNotFoundError(HEADER.EXTERNAL.SERVICE)
        else:
            return Activity(service=service, runtime=runtime)

    @inline_callbacks
    def _send_request_package(self, target, request_id, request_package):
        """
        :type target: L{pycloudia.cluster.beans.Activity}
        :type request_id: C{str}
        :type request_package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage}
        """
        timeout = self._get_external_timeout(request_package)
        response_package = yield self.sender.send_request_package(self, target, request_package, timeout)
        response_package = self._pop_internal_headers(response_package)
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

    @staticmethod
    def _pop_internal_headers(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        for header_name in package.headers.keys():
            if header_name.startswith(HEADER.INTERNAL_PREFIX):
                del package.headers[header_name]
        return package

    def _send_package(self, target, package):
        """
        :type target: L{pycloudia.cluster.beans.Activity}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
        self.sender.send_package(target, package)
