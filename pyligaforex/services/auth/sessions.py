from pyligaforex.services.auth.interfaces import ISessions


class Sessions(ISessions):
    """
    :type service: L{pyligaforex.services.gateways.interfaces.IService}
    """
    service = None

    def authenticate(self, client_id, user_id):
        return self.service.authenticate_gateway(client_id, user_id)


class SessionsFactory(object):
    """
    :type service_factory: C{Callable}
    :type adapter_factory: C{Callable}
    """
    service_factory = None
    adapter_factory = None

    def create_service(self):
        instance = Sessions()
        instance.service = self.service_factory()
        return instance

    def create_adapter(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        """
        instance = Sessions()
        instance.service = self.adapter_factory(source)
        return instance
