from abc import ABCMeta, abstractmethod


class IServiceFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_service(self):
        """
        :rtype: L{pyligaforex.services.gateways.interfaces.IService}
        """


class IService(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def create_gateway(self, channel):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def delete_gateway(self, runtime, reason=None):
        """
        :type runtime: C{str}
        :type reason: C{str} or C{None}
        :rtype: L{Deferred} of C{None}
        :raise: L{pyligaforex.services.gateways.exceptions.GatewayNotFoundError}
        """

    @abstractmethod
    def authenticate_gateway(self, runtime, user_id):
        """
        :type runtime: C{str}
        :type user_id: C{str}
        :rtype: L{Deferred} of C{None}
        :raise: L{pyligaforex.services.gateways.exceptions.GatewayNotFoundError}
        """

    @abstractmethod
    def process_incoming_package(self, runtime, package):
        """
        :type runtime: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        :raise: L{pyligaforex.services.gateways.exceptions.GatewayNotFoundError}
        """

    @abstractmethod
    def process_outgoing_package(self, runtime, package):
        """
        :type runtime: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        :raise: L{pyligaforex.services.gateways.exceptions.GatewayNotFoundError}
        """


class IGateway(object):
    __metaclass__ = ABCMeta

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
        :raise: L{pyligaforex.services.gateways.exceptions.HeaderNotFoundError}
        """

    @abstractmethod
    def process_outgoing_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        """


class IGatewayFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_gateway(self, channel):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        :rtype: L{pyligaforex.services.gateways.interfaces.IGateway}
        """


class IRouter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_target_channel(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{pycloudia.services.beans.Channel}
        :raise: L{pyligaforex.services.gateways.exceptions.HeaderNotFoundError}
        :raise: L{pyligaforex.services.gateways.exceptions.ServiceNotFoundError}
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


class IClients(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_outgoing_package(self, client_address, client_id, package):
        """
        :type client_address: C{str}
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        """
