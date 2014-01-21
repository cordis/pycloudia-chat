from pycloudia.cluster.exceptions import PackageError


class ActivityNotFoundError(PackageError):
    pass


class HeaderNotFoundError(PackageError):
    pass


class UserIdNotFoundError(Exception):
    pass
