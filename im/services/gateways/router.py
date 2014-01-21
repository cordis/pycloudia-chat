from im.services.gateways.consts import HEADER
from im.services.gateways.exceptions import ActivityNotFoundError, HeaderNotFoundError
from im.services.gateways.interfaces import IRouter


class Router(IRouter):
    """
    :type internal_request_id_factory: C{Callable}
    """
    internal_request_id_factory = None

    def __init__(self, gateway, sender, respondent):
        """
        :type gateway: L{im.services.gateways.interfaces.IRunner}
        :type sender: L{pycloudia.cluster.interfaces.ISender}
        :type respondent: L{pycloudia.respondent.interfaces.IRunner}
        """
        self.gateway = gateway
        self.sender = sender
        self.respondent = respondent

    def route_package(self, package):
        try:
            request_id = package.headers.pop(HEADER.EXTERNAL.REQUEST_ID)
        except KeyError:
            self._send_package(package)
        else:
            self._send_request_package(request_id, package)

    def _send_request_package(self, external_request_id, package):
        package.headers[HEADER.INTERNAL.REQUEST_ID] = internal_request_id = self.internal_request_id_factory()

    def _send_package(self, package):
        service = self._get_header(package, HEADER.SERVICE)
        command = self._get_header(package, HEADER.COMMAND)
        try:
            return self.service_map[service].route_package(command, package)
        except KeyError:
            raise ActivityNotFoundError(package, service)

    @staticmethod
    def _get_header(package, name):
        try:
            return package.headers[name]
        except KeyError:
            raise HeaderNotFoundError(package, name)
