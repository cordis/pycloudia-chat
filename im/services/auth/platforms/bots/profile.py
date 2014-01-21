from random import random

from im.services.auth.platforms.interfaces import IProfile


class Profile(IProfile):
    def __init__(self, access_token):
        """
        :type access_token: C{str}
        """
        self.access_token = access_token
        self.user_id = str(random())

    @property
    def name(self):
        return self.access_token

    @property
    def email(self):
        return None

    @property
    def avatar(self):
        return None

    @property
    def birthday(self):
        return None

    def language(self):
        return None
