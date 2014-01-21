from pycloudia.respondent.exceptions import ResponseTimeoutError
from pycloudia.uitls.defer import inline_callbacks, deferrable
from im.services.facades.exceptions import ClientNotFoundError
from im.services.gateways.consts import HEADER
from im.services.gateways.interfaces import IService
from im.services.gateways.runner import Runner


class Service(IService):
    """
    :type activities: L{pycloudia.cluster.beans.ActivityRegistry}
    :type facades: L{im.services.facades.interfaces.IService}
    :type runtime_factory: C{Callable}
    :type router: L{im.services.gateways.interfaces.IRouter}
    :type dao: L{im.services.gateways.interfaces.IDao}
    """
    activities = None

    facades = None

    runtime_factory = Runner
    router = None
    dao = None

    def __init__(self):
        self.runtime_map = {}

    @deferrable
    def initialize(self):
        pass

    @deferrable
    def create_gateway(self, client_id, facade_id):
        runtime = self.runtime_factory(client_id, facade_id)
        self.activities.contain(self, runtime)
        self.runtime_map[client_id] = runtime

    @inline_callbacks
    def suspend_activity(self, activity):
        del self.runtime_map[activity.runtime]

    @inline_callbacks
    def recover_activity(self, client_id, facade_id):
        user_id = yield self.dao.find_user_id_or_none(client_id)
        gateway = self.runtime_factory(client_id, facade_id, user_id)
        self.activities.contain(self, gateway)
        self.runtime_map[client_id] = gateway
        yield self._delete_gateway_if_required(facade_id, client_id)

    @inline_callbacks
    def _delete_gateway_if_required(self, facade_id, client_id):
        try:
            yield self.facades.validate(facade_id, client_id)
        except (ResponseTimeoutError, ClientNotFoundError) as e:
            yield self.delete_gateway(client_id, e)

    @deferrable
    def delete_gateway(self, client_id, reason=None):
        activity = self.runtime_map.pop(client_id)
        self.activities.discard(self, activity)

    @inline_callbacks
    def authenticate_gateway(self, client_id, user_id):
        runtime = self.runtime_map[client_id]
        runtime.user_id = yield self.dao.store_user_id(client_id, user_id)

    @inline_callbacks
    def process_incoming_package(self, client_id, package):
        runtime = self.runtime_map[client_id]
        package.headers[HEADER.USER_ID] = runtime.user_id
        package.headers[HEADER.CLIENT_ID] = runtime.client_id
        yield self.router.route_package(runtime, package)

    @deferrable
    def process_outgoing_package(self, client_id, package):
        runtime = self.runtime_map[client_id]
        package.headers.pop(HEADER.USER_ID, None)
        package.headers.pop(HEADER.CLIENT_ID, None)
        self.facades.process_outgoing_package(runtime.facade_id, runtime.client_id, package)
