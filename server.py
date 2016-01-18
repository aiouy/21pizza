#!/usr/bin/env python3
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from flask import Flask, request, jsonify

import urllib.request
import json
import requests

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def get_price(req):
    print(req.data)
    r = requests.post(url='http://localhost:3000/validateAndPrice', json=req.data)
    print('doing')
    response_status = json.loads(r.text)['result']['Status']
    print(response_status)

    if int(response_status) == 1 or int(response_status) == 0:
        price_in_usd = json.loads(r.text)['result']['Order']['Amounts']['Payment']
        print(price_in_usd)

        get_bitpay_btc_usd_rate = urllib.request.urlopen(url='https://bitpay.com/api/rates/usd').read().decode('utf-8')
        usd_per_btc = json.loads(get_bitpay_btc_usd_rate)['rate']
        print(price_in_usd)

        price = int(price_in_usd * 10**8 / usd_per_btc)
        print(price)
        # price = 100
    else:
        setattr(request, 'error_validate', 'error_validate')
        price = 0

    return price


@app.route('/order', methods=['POST'])
@payment.required(get_price)
def order():
    if hasattr(request, 'error_validate'):
        return bad_request('There is a problem with your order details.')

    return 'Pizza ordered!'


@app.route('/validate', methods=['POST'])
def validate():
    print(request.data)
    r = requests.post(url='http://localhost:3000/validateAndPrice', json=req.data)
    response_status = json.loads(r.text)['result']['Status']
    print(response_status)
    return 'awesome'
    # price = get_price(request)
    # return 'price = {0}'.format(price)

@app.route('/findNearbyStore', methods=['GET'])
def findNearbyStore():
    zip_code = request.args.get('zipCode')
    print(zip_code)
    some_url = 'http://localhost:3000/findStores/' + zip_code
    r = urllib.request.urlopen(url=some_url).read().decode('utf-8')
    returned_data = json.loads(r)
    print(returned_data)

    return 'awesome'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
