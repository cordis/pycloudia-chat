from tornado.web import RequestHandler, HTTPError

from pycloudia.uitls.defer import inline_callbacks, return_value
from pycloudia.uitls.decorators import generate_list

from pyligaforex.activities import Registry


class ResponseBuilder(object):
    @generate_list
    def build_currency_list(self, currency_list):
        for currency in currency_list:
            yield self.build_currency(currency)

    @staticmethod
    def build_currency(currency):
        return {
            'id': currency.guid,
            'comment': currency.comment,
            'interestRate': currency.rates.interest,
            'libid': currency.rates.bid,
            'libor': currency.rates.offered,
        }


class ItemHandler(RequestHandler):
    activities = Registry()
    response_builder = ResponseBuilder()

    @inline_callbacks
    def get(self, currency_id):
        currency_list = yield self.activities.currencies.get_any().get_currency_list()
        for currency in currency_list:
            if currency.guid == currency_id:
                return_value(self.response_builder.build_currency(currency))
        raise HTTPError(404, 'currency_not_found')


class ListHandler(RequestHandler):
    activities = Registry()
    response_builder = ResponseBuilder()

    @inline_callbacks
    def get(self, currency_id):
        currency_list = yield self.activities.currencies.get_any().get_currency_list()
        return_value(self.response_builder.build_currency_list(currency_list))
