from pycloudia.uitls.defer import inline_callbacks, deferrable, return_value

from im.services.consts import HEADER
from im.services.gateways.consts import DEFAULT
from im.services.gateways.interfaces import IGateway, IGatewayFactory


class Gateway(IGateway):
    """
    :type router: L{im.services.gateways.interfaces.IRouter}
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type source_factory: L{pycloudia.services.interfaces.IServiceChannelFactory}
    """
    router = None
    sender = None
    source_factory = None

    def __init__(self, channel):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        """
        self.channel = channel
        self.user_id = None
        self.source = self.source_factory.create_by_runtime(self.channel.runtime)

    def set_client_user_id(self, user_id):
        self.user_id = user_id

    @inline_callbacks
    def process_incoming_package(self, package):
        target = self.router.get_target_channel(package)
        package.headers[HEADER.INTERNAL.USER_ID] = self.user_id
        response_package = yield self._forward_package(target, package)
        if response_package is not None:
            self.process_outgoing_package(response_package)

    @deferrable
    def _forward_package(self, target, package):
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
    def _send_request_package(self, request_id, target, package):
        """
        :type request_id: C{str}
        :type target: L{pycloudia.services.beans.Channel}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage}
        """
        timeout = package.headers.pop(HEADER.EXTERNAL.TIMEOUT, DEFAULT.EXTERNAL.TIMEOUT)
        response_package = yield self.sender.send_request_package(self.source, target, package, timeout)
        response_package.headers[HEADER.EXTERNAL.RESPONSE_ID] = request_id
        return_value(response_package)

    @deferrable
    def process_outgoing_package(self, package):
        self._send_package(self.channel, package)

    def _send_package(self, target, package):
        """
        :type target: L{pycloudia.services.beans.Channel}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{None}
        """
        self.sender.send_package(target, package)


class GatewayFactory(IGatewayFactory):
    """
    :type dao: L{im.services.gateways.interfaces.IDao}
    """
    dao = None

    def create_gateway(self, channel):
        instance = Gateway(channel)
        instance.dao = self.dao
        return instance
