from pycloudia.uitls.defer import deferrable

from pyligaforex.services.users.interfaces import IService


class ClientProxy(IService):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    """
    sender = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.cluster.beans.Activity}
        """
        self.source = source

    @deferrable
    def create_or_update_online_user(self, user_id, client_id, platform, profile):
        pass
