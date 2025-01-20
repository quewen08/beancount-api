from flask import request
from flask_restx.resource import Resource
from flask_restx import fields
from beancount.core.number import D
from beancount.core import amount, data

from bapp.api.core import api
from bapp.core.storage import storage

ns = api.namespace('transaction', description='Transactions, 记录交易信息，并生成对应的beancount文件')

posting_model = api.model('Posting', {
    'account': fields.String(required=True, description='Account of the posting, 账户名称'),
    'amount': fields.Arbitrary(description='Amount, 金额'),
    'currency': fields.String(description='Currency, 货币'),
    'cost': fields.Arbitrary(description='Cost 成本'),
    'costCurrency': fields.String(description='Cost Currency (Option) 转换成成本的货币'),
})

trx_add_model = api.model('TransactionAdd', {
    'filename': fields.String(required=True, description='Filename of the file，不可以为空'),
    'date': fields.Date(required=True, description='Date of the transaction，交易日期，默认今天'),
    'flag': fields.String(enum=['*', '!'], default='*', description='Flag for the transaction, 默认 *'),
    'payee': fields.String('Payee of the transaction, 收款人'),
    'naration': fields.String('Naration of the transaction, 备注'),
    'postings': fields.List(fields.Nested(posting_model)),
})


@ns.route('/')
class Transaction(Resource):

    @api.expect(trx_add_model, validate=True)
    def put(self):
        requestData = request.json

        postings = []
        for reqPost in requestData['postings']:
            if 'cost' in reqPost and 'costCurrency' in reqPost:
                cost = data.CostSpec(
                    D(str(reqPost['cost'])),
                    None,
                    reqPost['costCurrency'],
                    None,
                    None,
                    None
                )
            else:
                cost = None

            if 'amount' in reqPost and 'currency' in reqPost:
                amt = amount.Amount(D(str(reqPost['amount'])), reqPost['currency'])
            else:
                amt = None

            postings.append(data.Posting(
                reqPost['account'],
                amt,
                cost,
                None,
                None,
                None
            ))
        print(requestData)
        storage.add_transaction(
            data.Transaction(
                None,
                requestData['date'],
                requestData.get('flag', '*'),
                requestData.get('payee', None),
                requestData.get('naration', None),
                None,
                None,
                postings
            ),
            requestData['filename']
        )

        return 'ok'
