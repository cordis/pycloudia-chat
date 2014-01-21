from pycloudia.cluster.exceptions import PackageError


class ActivityNotFoundError(PackageError):
    pass


class HeaderNotFoundError(PackageError):
    pass


class UserIdNotFoundError(Exception):
    pass


class GatewayNotFoundError(Exception):
    def __init__(self, client_id, *args, **kwargs):
        self.client_id = client_id
        super(GatewayNotFoundError, self).__init__(*args, **kwargs)
