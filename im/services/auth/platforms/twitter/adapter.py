from im.services.auth.platforms.interfaces import IAdapter


class Adapter(IAdapter):
    def get_friends(self, access_token, profile):
        raise NotImplementedError()

    def authenticate(self, access_token):
        raise NotImplementedError()
