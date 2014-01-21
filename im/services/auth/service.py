from pycloudia.reactor.decorators import call_isolated
from pycloudia.uitls.defer import inline_callbacks, return_value

from im.services.auth.interfaces import IService


class Service(IService):
    """
    :type users: L{im.services.users.interfaces.IService}
    :type gateways: L{im.services.gateways.interfaces.IService}
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type adapters: L{im.services.auth.platforms.interfaces.IAdapterRegistry}
    :type dao: L{im.services.auth.interfaces.IDao}
    """
    users = None
    gateways = None

    reactor = None

    adapters = None
    dao = None

    @call_isolated
    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        adapter = self.adapters.get_adapter(platform)
        profile = yield adapter.authenticate(access_token)
        user_id, created = yield self.dao.get_or_create_user(platform, profile)
        if created:
            self.reactor.call(self._retrieve_platform_friends, user_id, platform, profile)
        yield self.users.create_or_update_online_user(user_id, client_id, platform, profile)
        yield self.gateways.authenticate_gateway(client_id, user_id)
        return_value(profile)

    @inline_callbacks
    def _retrieve_platform_friends(self, user_id, platform, profile):
        adapter = self.adapters.get_adapter(platform)
        profile_list = yield adapter.get_friends(profile)
        yield self.dao.set_user_friends(user_id, platform, profile_list)
