from pyligaforex.services.consts import HEADER
from pyligaforex.services.gateways.interfaces import IRouter
from pyligaforex.services.gateways.exceptions import HeaderNotFoundError, ServiceNotFoundError


class Router(IRouter):
    """
    :type adapter_map: C{dict}
    """
    adapter_map = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        """
        self.source = source

    def get_target_channel(self, package):
        service = self._pop_service(package)
        adapter = self._get_service_adapter(service)
        return adapter.get_target_channel(package)

    @staticmethod
    def _pop_service(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: C{str}
        :raise: L{pyligaforex.services.gateways.exceptions.HeaderNotFoundError}
        """
        try:
            return package.headers.pop(HEADER.EXTERNAL.SERVICE)
        except KeyError:
            raise HeaderNotFoundError(HEADER.EXTERNAL.SERVICE)

    def _get_service_adapter(self, service):
        """
        :type service: C{str}
        :rtype: L{***}
        :raise: L{pyligaforex.services.gateways.exceptions.ServiceNotFoundError}
        """
        try:
            return self.adapter_map[service]
        except KeyError:
            raise ServiceNotFoundError(service)
