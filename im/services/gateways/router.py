from pycloudia.uitls.defer import deferrable, inline_callbacks, return_value

from im.services.consts import HEADER
from im.services.gateways.consts import DEFAULT
from im.services.gateways.interfaces import IRouter
from im.services.gateways.exceptions import HeaderNotFoundError


class Router(IRouter):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type target_factory: L{pycloudia.services.interfaces.IChannelsFactory}
    """
    sender = None
    target_factory = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        """
        self.source = source

    @deferrable
    def route_package(self, package):
        target = self._pop_external_target(package)
        package = self._copy_external_command(package)
        return self._route_package(target, package)

    def _pop_external_target(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: C{pycloudia.services.beans.Channel}
        :raise: L{im.services.gateways.exceptions.HeaderNotFoundError}
        """
        try:
            service = package.headers.pop(HEADER.EXTERNAL.SERVICE)
        except KeyError:
            raise HeaderNotFoundError(HEADER.EXTERNAL.SERVICE)
        else:
            runtime = package.headers.pop(HEADER.EXTERNAL.RUNTIME, HEADER.INTERNAL.CLIENT_ID)
            return self.target_factory.create_by_runtime(service, runtime)

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

    def _route_package(self, target, package):
        """
        :type target: L{pycloudia.services.beans.Channel}
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
        :type target: L{pycloudia.services.beans.Channel}
        :type request_package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage}
        """
        timeout = self._get_external_timeout(request_package)
        response_package = yield self.sender.send_request_package(self.source, target, request_package, timeout)
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
        :type target: L{pycloudia.services.beans.Channel}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
        self.sender.send_package(target, package)
