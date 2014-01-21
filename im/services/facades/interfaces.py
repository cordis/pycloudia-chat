from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_outgoing_package(self, address, client_id, package):
        """
        :type address: C{str}
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IListener(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, director):
        """
        :type director: L{im.services.facades.interfaces.IDirector}
        :raises L{im.services.facades.exceptions.ListenFailedError}
        """


class IClientIdFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self):
        """
        :rtype: C{str}
        """


class IClient(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_message(self, message):
        """
        :type message: C{str}
        """


class IDirector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def connection_made(self, client):
        """
        :type client: C{IClient}
        """

    @abstractmethod
    def connection_done(self, client):
        """
        :type client: C{IClient}
        """

    @abstractmethod
    def connection_lost(self, client, reason):
        """
        :type client: C{IClient}
        :type reason: C{str}
        """

    @abstractmethod
    def read_message(self, client, message):
        """
        :type client: C{IClient}
        :type str message:
        """
