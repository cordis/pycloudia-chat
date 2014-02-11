from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_contacts(self, user_id, limit=None, offset=None):
        """
        :type user_id: C{str}
        :type limit: C{int} or C{None}
        :type offset: C{str} or C{None}
        """

    @abstractmethod
    def update_contact(self, user_id, thread, count=1):
        """
        :type user_id: C{str}
        :type thread: L{pyligaforex.services.contacts.interfaces.IChatIdentity}
        :type count: C{int}
        """

    @abstractmethod
    def delete_contact(self, user_id, thread):
        """
        :type user_id: C{str}
        :type thread: L{pyligaforex.services.contacts.interfaces.IChatIdentity}
        """


class IChatIdentity(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        """
        :rtype: C{str}
        """
