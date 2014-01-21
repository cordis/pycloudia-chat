from abc import ABCMeta, abstractmethod, abstractproperty


class IProfile(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def user_id(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def name(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def email(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def avatar(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def birthday(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def language(self):
        """
        :rtype: C{str}
        """


class IAdapter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self, access_token):
        """
        :type access_token: C{str}
        :rtype: L{im.services.auth.platforms.interfaces.IProfile}
        """

    @abstractmethod
    def get_friends(self, access_token, profile):
        """
        :type access_token: C{str}
        :type profile: L{im.services.auth.platforms.interfaces.IProfile}
        :rtype: C{list} of L{im.services.auth.platforms.interfaces.IProfile}
        """


class IAdapterRegistry(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_adapter(self, platform):
        """
        :type platform: C{str}
        :rtype: L{im.services.auth.platforms.interfaces.IAdapter}
        """
