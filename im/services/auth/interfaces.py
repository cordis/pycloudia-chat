from abc import ABCMeta, abstractmethod


class IServiceFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self):
        """
        :rtype: L{im.services.auth.interfaces.IService}
        """


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
        :rtype: L{Deferred} of C{None}
        """
        
        
class ISessionsFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_service(self):
        """
        :rtype: L{im.services.auth.interfaces.ISessions}
        """

    @abstractmethod
    def create_adapter(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        :rtype: L{im.services.auth.interfaces.ISessions}
        """


class ISessions(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :rtype: L{Deferred} of C{None}
        """


class IUsersFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_service(self):
        """
        :rtype: L{im.services.auth.interfaces.IUsers}
        """

    @abstractmethod
    def create_adapter(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        :rtype: L{im.services.auth.interfaces.IUsers}
        """


class IUsers(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self, user_id, client_id, platform, profile):
        """
        :type user_id: C{str}
        :type client_id: C{str}
        :type platform: C{str}
        :type profile: L{im.services.auth.platforms.interfaces.IProfile}
        :rtype: L{Deferred} of C{None}
        """


class IPlatforms(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, platform):
        """
        :type platform: C{str}
        :rtype: L{im.services.auth.platforms.interfaces.IAdapter}
        :raise: C{KeyError}
        """
