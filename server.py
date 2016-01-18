#!/usr/bin/env python3
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from flask import Flask, request, jsonify

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def get_price(request):
    bad_arguments = []
    # if not request.args.get('address'):
    #     bad_arguments.append('address')

    if not len(bad_arguments):
        price = 10  # validator
    else:
        setattr(request, 'bad_arguments', bad_arguments)
        price = 0

    return price


@app.route('/order', methods=['POST'])
@payment.required(get_price)
def order():
    return request.data


@app.route('/validate')
@payment.required(1)
def validate():
    return 'nothing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
