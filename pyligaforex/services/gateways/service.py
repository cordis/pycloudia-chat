from pycloudia.uitls.defer import inline_callbacks, deferrable
from pycloudia.reactor.decorators import call_isolated

from pyligaforex.services.gateways.interfaces import IService, IServiceFactory
from pyligaforex.services.gateways.exceptions import GatewayNotFoundError


class Service(IService):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type gateway_factory: C{pyligaforex.services.gateways.interfaces.IGatewayFactory}
    """
    reactor = None
    gateway_factory = None

    def __init__(self):
        self.gateway_map = {}

    @deferrable
    def initialize(self):
        pass

    @call_isolated
    @inline_callbacks
    def create_gateway(self, channel):
        self.gateway_map[channel.runtime] = self.gateway_factory.create_gateway(channel)

    @call_isolated
    @deferrable
    def authenticate_gateway(self, runtime, user_id):
        return self._get_gateway(runtime).set_client_user_id(user_id)

    def process_incoming_package(self, runtime, package):
        return self._get_gateway(runtime).process_incoming_package(package)

    def process_outgoing_package(self, runtime, package):
        return self._get_gateway(runtime).process_outgoing_package(package)

    def _get_gateway(self, runtime):
        """
        :type runtime: C{str}
        :rtype: L{pyligaforex.services.gateways.interfaces.IGateway}
        :raise: L{pyligaforex.services.gateways.exceptions.GatewayNotFoundError}
        """
        try:
            return self.gateway_map[runtime]
        except KeyError:
            raise GatewayNotFoundError(runtime)

    @call_isolated
    @deferrable
    def delete_gateway(self, runtime, reason=None):
        try:
            gateway = self.gateway_map.pop(runtime)
        except KeyError:
            pass
        else:
            return gateway.destroy(reason)


class ServiceFactory(IServiceFactory):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type gateway_factory: C{pyligaforex.services.gateways.interfaces.IGatewayFactory}
    """
    reactor = None
    gateway_factory = None

    def create_service(self):
        instance = Service()
        instance.reactor = self.reactor
        instance.gateway_factory = self.gateway_factory
        return instance
