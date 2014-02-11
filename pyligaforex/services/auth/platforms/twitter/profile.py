from pyligaforex.services.auth.platforms.interfaces import IProfile


class Profile(IProfile):
    def __init__(self, info):
        """
        :type info: C{dict}
        """
        self.info = info

    @property
    def user_id(self):
        return self.info['id_str']

    @property
    def name(self):
        return self.info['name']

    @property
    def email(self):
        return None

    @property
    def avatar(self):
        return self.info.get('profile_image_url', None)

    @property
    def birthday(self):
        return None

    def language(self):
        return self.info['lang']
