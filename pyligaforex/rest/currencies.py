from tornado.web import RequestHandler

from pyligaforex.rest.decorators import http_error, http_jsonify, http_jsonify_list, http_request_handler
from pyligaforex.activities import Registry
from pyligaforex.services.currencies.exceptions import CurrencyNotFoundError, CurrencyBaseError


class ResponseBuilder(object):
    @staticmethod
    def jsonify_currency(currency):
        return {
            'id': currency.guid,
            'name': currency.name,
            'libid': currency.rates.bid,
            'libor': currency.rates.offered,
            'interestRate': currency.rates.interest,
            'comment': currency.comment,
        }


@http_request_handler
class ItemHandler(object):
    activities = Registry()
    response_builder = ResponseBuilder()

    @http_error(CurrencyNotFoundError, 404)
    @http_error(CurrencyBaseError, 400)
    @http_jsonify(ResponseBuilder.jsonify_currency)
    def get(self, currency_id):
        return self.activities.currencies.get_any().get_currency(currency_id)


@http_request_handler
class ListHandler(RequestHandler):
    activities = Registry()
    response_builder = ResponseBuilder()

    @http_error(CurrencyBaseError, 400)
    @http_jsonify_list(ResponseBuilder.jsonify_currency)
    def get(self):
        return self.activities.currencies.get_any().get_currency_list()
