from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def create_gateway(self, client_id, facade_address):
        """
        :type client_id: C{str}
        :type facade_address: C{str}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def delete_gateway(self, client_id, reason=None):
        """
        :type client_id: C{str}
        :type reason: C{str}
        :rtype: L{Deferred} of C{None}
        :raise: L{im.services.gateways.exceptions.GatewayNotFoundError}
        """

    @abstractmethod
    def authenticate_gateway(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :rtype: L{Deferred} of C{None}
        :raise: L{im.services.gateways.exceptions.GatewayNotFoundError}
        """

    @abstractmethod
    def process_incoming_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        :raise: L{im.services.gateways.exceptions.GatewayNotFoundError}
        """

    @abstractmethod
    def process_outgoing_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        :raise: L{im.services.gateways.exceptions.GatewayNotFoundError}
        """


class IRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_client_address(self, facade_address):
        """
        :type facade_address: C{str}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def set_client_user_id(self, user_id):
        """
        :type user_id: C{str}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def process_incoming_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        :raise: L{im.services.gateways.exceptions.HeaderNotFoundError}
        """

    @abstractmethod
    def process_outgoing_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        """


class IRunnerFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, client_id):
        """
        :type client_id: C{str}
        :rtype: L{im.services.gateways.interfaces.IRunner}
        """


class IRouter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def route_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage or None}
        :raise: L{im.services.gateways.exceptions.HeaderNotFoundError}
        """


class IDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_gateway_client_address(self, client_id, facade_address):
        """
        :type client_id: C{str}
        :type facade_address: C{str}
        :return: deferred with facade_address
        :rtype: L{Deferred} of C{str}
        """
        
    @abstractmethod
    def set_gateway_client_user_id(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :return: deferred with user_id
        :rtype: L{Deferred} of C{str}
        """
