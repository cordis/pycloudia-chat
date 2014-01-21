from pycloudia.uitls.structs import AbstractRegistry

from im.services.auth.platforms.interfaces import IAdapterRegistry


class Registry(AbstractRegistry, IAdapterRegistry):
    pass
