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
        """

    @abstractmethod
    def authenticate_gateway(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def process_incoming_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def process_outgoing_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
        """


class IRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_activity(self):
        """
        :rtype: L{pycloudia.cluster.beans.Activity}
        """

    @abstractmethod
    def set_facade_address(self, facade_address):
        """
        :type facade_address: C{str}
        :rtype: L{Deferred} of C{None}
        """
        
    @abstractmethod
    def set_user_id(self, user_id):
        """
        :type user_id: C{str}
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def process_incoming_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of C{None}
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


class IDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_gateway_facade_address(self, client_id, facade_address):
        """
        :type client_id: C{str}
        :type facade_address: C{str}
        :return: deferred with facade_address
        :rtype: L{Deferred} of C{str}
        """
        
    @abstractmethod
    def set_gateway_user_id(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :return: deferred with user_id
        :rtype: L{Deferred} of C{str}
        """
