from pycloudia.uitls.defer import deferrable

from pyligaforex.services.gateways.interfaces import IDao


class Dao(IDao):
    @deferrable
    def set_gateway_client_address(self, client_id, facade_address):
        return facade_address

    @deferrable
    def set_gateway_client_user_id(self, client_id, user_id):
        return user_id
