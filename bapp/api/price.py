from flask import request
from flask_restx.resource import Resource
from flask_restx import fields
from beancount.core.number import D
from beancount.core import amount, data

from bapp.api.core import api
from bapp.core.storage import storage

# 添加其他货币(多币种)
ns = api.namespace('price', description='Prices，添加其他货币(多币种)')

price_model = api.model('Price', {
    'date': fields.Date(required=True, description='Date of the price'),
    'quoteCurrency': fields.String(required=True, description='Currency to be priced'),
    'baseCurrency': fields.String(required=True, description='Base currency the price is in'),
    'price': fields.Arbitrary(required=True, description='Price')
})

prices_update_model = api.model('PriceUpdate', {
    'filename': fields.String(required=True, description='Filename of the price file'),
    'prices' : fields.List(fields.Nested(price_model)),
})

@ns.route('/')
class Price(Resource):

    @api.expect(prices_update_model, validate=True)
    def post(self):
        prices = []
        requestData = request.json
        
        for requestPrice in requestData['prices']:
            prices.append(data.Price(
                None,
                requestPrice['date'],
                requestPrice['quoteCurrency'],
                amount.Amount(D(str(requestPrice['price'])), requestPrice['baseCurrency'])))

        storage.set_price(prices, requestData['filename'])
        
        return 'ok'