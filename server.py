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
    # r = request.post(url='http://localhost:3000/validateAndPrice', json=request.data)
    status = 'error'

    if status == 'success':
        price = 100
    else:
        setattr(request, 'error_validate', 'error_validate')
        price = 0

    return price


@app.route('/order', methods=['POST'])
@payment.required(get_price)
def order():
    if hasattr(request, 'error_validate'):
        return bad_request('There is a problem with your order details.')
    return request.data


@app.route('/validate')
@payment.required(1)
def validate():
    return 'nothing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
