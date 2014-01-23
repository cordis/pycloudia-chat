from pycloudia.cluster.beans import Activity

from im.services.facades.interfaces import IService
from im.services.facades.consts import SERVICE, HEADER
from pycloudia.services.interfaces import IInvoker


class ClientProxy(IService):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    """
    sender = None

    def process_outgoing_package(self, address, client_id, package):
        target = self._create_target_activity(address)
        package.headers[HEADER.ADDRESS] = address
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package(target, package)

    @staticmethod
    def _create_target_activity(address):
        return Activity(service=SERVICE.NAME, address=address)


class ServerProxy(IInvoker):
    def __init__(self, service):
        """
        :type service: L{im.services.facades.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        address = package.headers.pop(HEADER.ADDRESS)
        client_id = package.headers.pop(HEADER.CLIENT_ID)
        self.service.process_outgoing_package(address, client_id, package)
