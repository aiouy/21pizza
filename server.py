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


# Validation & get price. Runs through domino validation call and returns the price of the order if valid, else price=0
def get_price(request):
    r = requests.post(url='http://localhost:3000/validateAndPrice', json=json.loads(request.data))
    response_status = json.loads(r.text)['result']['Status']

    if int(response_status) == 1 or int(response_status) == 0: # not sure what the dominos api response codes are but these seem to not err
        price_in_usd = json.loads(r.text)['result']['Order'][
            'Amounts']['Payment']

        get_bitpay_btc_usd_rate = urllib.request.urlopen(url='https://bitpay.com/api/rates/usd').read().decode('utf-8')
        usd_per_btc = json.loads(get_bitpay_btc_usd_rate)['rate']

        price = int(price_in_usd * 10**8 / usd_per_btc)
        print(price)
    else:
        setattr(request, 'error_validate', 'error_validate')
        price = 0

    return price

# Orders the pizza. Should pass the user though /validate first but this will run a validation check as well
@app.route('/order', methods=['POST'])
@payment.required(get_price) # get_price function call. If order is invalid, the user is not charged.
def order():
    if hasattr(request, 'error_validate'):
        return bad_request('There is a problem with your order details.')

    # TODO: call order function on order.js
    return 'Pizza ordered!' # TODO: Add response details


# Runs dominos validate function and should return price if the order details are valid, else return error
@app.route('/validate', methods=['POST'])
def validate():
    price = get_price(request)
    return 'price = {0}'.format(price) # TODO: return error if price = 0


# Find stores near user's ZIP
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
