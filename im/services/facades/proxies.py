from pycloudia.services.interfaces import IInvoker

from im.services.facades.interfaces import IService
from im.services.facades.consts import HEADER


class ClientProxy(IService):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type target_factory: L{pycloudia.services.interfaces.IServiceChannelFactory}
    """
    sender = None
    target_factory = None

    def process_outgoing_package(self, address, client_id, package):
        target = self.target_factory.create_by_address(address)
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package(target, package)


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
