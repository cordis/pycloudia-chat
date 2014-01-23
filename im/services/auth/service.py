from pycloudia.reactor.decorators import call_isolated
from pycloudia.uitls.defer import inline_callbacks, return_value

from im.services.auth.interfaces import IService


class Service(IService):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type dao: L{im.services.auth.interfaces.IDao}
    :type users: L{im.services.auth.interfaces.IUsers}
    :type sessions: L{im.services.auth.interfaces.ISessions}
    :type platforms: L{im.services.auth.interfaces.IPlatforms}
    """
    reactor = None
    dao = None
    users = None
    sessions = None
    platforms = None

    @call_isolated
    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        adapter = self.platforms.get(platform)
        profile = yield adapter.authenticate(access_token)
        user_id, created = yield self.dao.get_or_create_user(platform, profile)
        if created:
            self.reactor.call(self._retrieve_platform_friends, user_id, platform, profile)
        yield self.users.authenticate(user_id, client_id, platform, profile)
        yield self.sessions.authenticate(client_id, user_id)
        return_value(profile)

    @call_isolated
    @inline_callbacks
    def _retrieve_platform_friends(self, user_id, platform, profile):
        adapter = self.platforms.get(platform)
        profile_list = yield adapter.get_friends(profile)
        yield self.dao.set_user_friends(user_id, platform, profile_list)


class ServiceFactory(object):
    """
    :type dao: L{im.services.auth.interfaces.IDao}
    :type reactor: L{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type platforms: L{im.services.auth.interfaces.IPlatforms}
    """
    dao = None
    reactor = None
    platforms = None

    def __call__(self):
        instance = Service()
        instance.dao = self.dao
        instance.reactor = self.reactor
        instance.platforms = self.platforms
        return instance
