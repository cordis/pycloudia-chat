from im.services.auth.interfaces import IUsers


class Users(IUsers):
    """
    :type service: L{im.services.users.interfaces.IService}
    """
    service = None

    def authenticate(self, user_id, client_id, platform, profile):
        return self.service.create_or_update_online_user(user_id, client_id, platform, profile)


class UsersFactory(object):
    """
    :type service_factory: C{Callable}
    :type adapter_factory: C{Callable}
    """
    service_factory = None
    adapter_factory = None

    def create_service(self):
        instance = Users()
        instance.service = self.service_factory()
        return instance

    def create_adapter(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        """
        instance = Users()
        instance.service = self.adapter_factory(source)
        return instance
