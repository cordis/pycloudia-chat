from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_or_update_online_user(self, user_id, client_id, platform, profile):
        """
        :type user_id: C{str}
        :type client_id: C{str}
        :type platform: C{str}
        :type profile: L{pyligaforex.services.auth.platforms.interfaces.IProfile}
        :rtype: L{Deferred} of C{None}
        """
