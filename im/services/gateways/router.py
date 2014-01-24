from im.services.consts import HEADER
from im.services.gateways.interfaces import IRouter
from im.services.gateways.exceptions import HeaderNotFoundError, ServiceNotFoundError


class Router(IRouter):
    """
    :type invoker_map: C{dict}
    """
    invoker_map = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        """
        self.source = source

    def get_target_channel(self, package):
        service = self._pop_service(package)
        invoker = self._get_service_invoker(service)
        return invoker.get_target_channel(package)

    @staticmethod
    def _pop_service(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: C{str}
        :raise: L{im.services.gateways.exceptions.HeaderNotFoundError}
        """
        try:
            return package.headers.pop(HEADER.EXTERNAL.SERVICE)
        except KeyError:
            raise HeaderNotFoundError(HEADER.EXTERNAL.SERVICE)

    def _get_service_invoker(self, service):
        """
        :type service: C{str}
        :rtype: L{***}
        :raise: L{im.services.gateways.exceptions.ServiceNotFoundError}
        """
        try:
            return self.invoker_map[service]
        except KeyError:
            raise ServiceNotFoundError(service)
