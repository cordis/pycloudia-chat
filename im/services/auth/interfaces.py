from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self, client_id, platform, access_token):
        """
        :type client_id: C{str}
        :type platform: C{str}
        :type access_token: C{str}
        :rtype: L{Deferred} of L{im.services.auth.platforms.interfaces.IProfile}
        :raise: L{im.services.auth.exceptions.AuthError}
        """


class IDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_or_create_user(self, platform, profile):
        """
        :type platform: C{str}
        :type profile: L{im.services.auth.platforms.interfaces.IProfile}
        :return: Deferred with Tuple of (user_id, created)
        :rtype: L{Deferred} of (C{str}, C{boolean})
        """

    @abstractmethod
    def set_user_friends(self, user_id, platform, profile_list):
        """
        :type user_id: C{str}
        :type platform: C{str}
        :type profile_list: C{list} of L{im.services.auth.platforms.interfaces.IProfile}
        """
