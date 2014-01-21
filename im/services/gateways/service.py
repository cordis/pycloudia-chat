from pycloudia.uitls.defer import inline_callbacks, deferrable
from pycloudia.reactor.decorators import call_isolated

from im.services.gateways.consts import HEADER
from im.services.gateways.interfaces import IService
from im.services.gateways.exceptions import GatewayNotFoundError


class Service(IService):
    """
    :type activities: L{pycloudia.cluster.beans.ActivityRegistry}
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type runner_factory: C{im.services.gateways.interfaces.IRunnerFactory}
    """
    activities = None

    reactor = None

    runner_factory = None

    def __init__(self):
        self.runner_map = {}

    @deferrable
    def initialize(self):
        pass

    @call_isolated
    @inline_callbacks
    def create_gateway(self, client_id, facade_address):
        runner = self.runner_factory(client_id)
        yield self.activities.attach(runner.get_activity())
        yield runner.set_facade_address(facade_address)
        self.runner_map[client_id] = runner

    @call_isolated
    @inline_callbacks
    def delete_gateway(self, client_id, reason=None):
        runner = self._get_runner(client_id)
        yield self.activities.detach(self, runner.get_activity())
        runner = self.runner_map.pop(client_id)
        yield runner.destroy(reason)

    @call_isolated
    @deferrable
    def authenticate_gateway(self, client_id, user_id):
        return self._get_runner(client_id).set_user_id(user_id)

    @deferrable
    def process_incoming_package(self, client_id, package):
        return self._get_runner(client_id).process_incoming_package(package)

    @deferrable
    def process_outgoing_package(self, client_id, package):
        return self._get_runner(client_id).process_outgoing_package(package)

    def _get_runner(self, client_id):
        try:
            return self.runner_map[client_id]
        except KeyError:
            raise GatewayNotFoundError(client_id)
