from pyligaforex.services.currencies.service import ServiceFactory as CurrenciesFactory
from pycloudia.activities.bases import BaseRegistry


class Activity(object):
    def __init__(self, factory):
        self.factory = factory


class Service(Activity):
    def find(self, address):
        raise NotImplementedError()


class Runtime(Activity):
    def find(self, guid):
        raise NotImplementedError()


class Registry(BaseRegistry):
    currencies = Service(CurrenciesFactory)
    orders = Runtime()
