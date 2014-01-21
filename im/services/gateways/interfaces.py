from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def create_gateway(self, client_id, facade_id):
        """
        :type client_id: C{str}
        :type facade_id: C{str}
        :rtype: L{Deferred}
        """

    @abstractmethod
    def delete_gateway(self, client_id, reason=None):
        """
        :type client_id: C{str}
        :type reason: C{str}
        :rtype: L{Deferred}
        """

    @abstractmethod
    def authenticate_gateway(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :rtype: L{Deferred}
        """

    @abstractmethod
    def process_incoming_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred}
        """

    @abstractmethod
    def process_outgoing_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred}
        """


class IRunner(object):
    __metaclass__ = ABCMeta


class IRouter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def route_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_user_id(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :return: deferred user_id
        :rtype: L{Deferred} of C{str}
        """

    @abstractmethod
    def find_user_id_or_none(self, client_id):
        """
        :type client_id: C{str}
        :return: deferred user_id
        :rtype: L{Deferred} of C{str}
        """
