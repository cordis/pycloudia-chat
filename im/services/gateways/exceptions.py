class BaseGatewayError(Exception):
    pass


class HeaderNotFoundError(BaseGatewayError):
    def __init__(self, header_name, *args, **kwargs):
        self.header_name = header_name
        super(HeaderNotFoundError, self).__init__(*args, **kwargs)


class GatewayNotFoundError(BaseGatewayError):
    def __init__(self, client_id, *args, **kwargs):
        self.client_id = client_id
        super(GatewayNotFoundError, self).__init__(*args, **kwargs)
