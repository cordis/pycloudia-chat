from pycloudia.uitls.defer import deferrable

from pyligaforex.services.auth.interfaces import IDao


class Dao(IDao):
    @deferrable
    def set_user_friends(self, user_id, platform, profile_list):
        pass

    @deferrable
    def get_or_create_user(self, platform, profile):
        return '.'.join([platform, profile.user_id]), True
