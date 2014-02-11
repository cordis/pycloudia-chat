from abc import ABCMeta, abstractmethod, abstractproperty


class IAdapter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self, access_token):
        """
        :type access_token: C{str}
        :rtype: L{Deferred} of L{pyligaforex.services.auth.platforms.interfaces.IProfile}
        """

    @abstractmethod
    def get_friends(self, access_token, profile):
        """
        :type access_token: C{str}
        :type profile: L{pyligaforex.services.auth.platforms.interfaces.IProfile}
        :rtype: L{Deferred} of C{list} of L{pyligaforex.services.auth.platforms.interfaces.IProfile}
        """


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
