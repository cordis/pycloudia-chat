from pycloudia.uitls.defer import deferrable

from im.services.auth.platforms.interfaces import IAdapter
from im.services.auth.platforms.bots.profile import Profile


class Adapter(IAdapter):
    @deferrable
    def get_friends(self, access_token, profile):
        return []

    @deferrable
    def authenticate(self, access_token):
        return Profile(access_token)
