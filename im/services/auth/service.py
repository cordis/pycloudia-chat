from im.services.auth.consts import SERVICE
from pycloudia.cluster.beans import Activity
from pycloudia.reactor.decorators import call_isolated
from pycloudia.uitls.defer import inline_callbacks, return_value

from im.services.auth.interfaces import IService


class Service(IService):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type dao: L{im.services.auth.interfaces.IDao}
    :type adapters: L{im.services.auth.platforms.interfaces.IAdapterRegistry}
    :type gateways: L{im.services.gateways.interfaces.IService}
    :type users: L{im.services.users.interfaces.IService}
    """
    reactor = None
    dao = None
    adapters = None

    gateways = None
    users = None

    def __init__(self, address):
        self.address = address

    def get_activity(self):
        return Activity(service=SERVICE.NAME, address=self.address)

    @call_isolated
    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        adapter = self.adapters.get(platform)
        profile = yield adapter.authenticate(access_token)
        user_id, created = yield self.dao.get_or_create_user(platform, profile)
        if created:
            self.reactor.call(self._retrieve_platform_friends, user_id, platform, profile)
        yield self.users.create_or_update_online_user(user_id, client_id, platform, profile)
        yield self.gateways.authenticate_gateway(client_id, user_id)
        return_value(profile)

    @inline_callbacks
    def _retrieve_platform_friends(self, user_id, platform, profile):
        adapter = self.adapters.get(platform)
        profile_list = yield adapter.get_friends(profile)
        yield self.dao.set_user_friends(user_id, platform, profile_list)
