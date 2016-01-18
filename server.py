#!/usr/bin/env python3
import json
import urllib.request as request
from flask import Flask

# Import from the 21 Bitcoin Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def get_price(request):
    bad_arguments = []
    if not request.args.get('address'):
        bad_arguments.append('address')

    if not len(bad_arguments):
        price =  10# validator
    else:
        setattr(request, 'bad_arguments', bad_arguments)
        price = 0

    return price


@app.route('/order')
@payment.required(get_price)
def order():
    bad_arguments = getattr(request, 'bad_arguments')
    if hasattr(request, 'bad_arguments'):
        return bad_request('Invalid request. Please check your argument(s): {}'.format(', '.join(bad_arguments)))

    return 'Awesome'


@app.route('/validate')
@payment.required(1)
def validate():
    return 'nothing'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
