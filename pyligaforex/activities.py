from pyligaforex.services.currencies.service import ServiceFactory as CurrenciesFactory
from pycloudia.activities.bases import BaseRegistry, Service, Runtime


class Registry(BaseRegistry):
    currencies = Service(CurrenciesFactory)
