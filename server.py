#!/usr/bin/env python3
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from flask import Flask, request, jsonify

import json
import requests

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

EXPRESS_SERVER = 'http://localhost:3000/'


def bad_request(message):
    response = json.dumps({'error': message})
    return response

def usd_per_btc():
    return requests.get('https://bitpay.com/api/rates/usd').json()['rate']

def usd_to_satoshi(price_in_usd):
    return price_in_usd * 10**8 / usd_per_btc()

# check validation and return dominos' response
def dominos_validation(request):
    return requests.post(url=EXPRESS_SERVER + 'validateAndPrice',
                      json=json.loads(request.get_data(as_text=True)))


# Validation & get price. Runs through domino validation call and returns
# the price of the order if valid, else price=0
def get_price(request):
    r = dominos_validation(request)
    response_status = json.loads(r.text)['result']['Status']

    # not sure what the dominos api response codes are but these seem to not
    # err
    if int(response_status) == 1 or int(response_status) == 0:
        price_in_usd = json.loads(r.text)['result']['Order'][
            'Amounts']['Payment']

        price = int(usd_to_satoshi(price_in_usd))
    else:
        setattr(request, 'error_validate', 'error_validate')
        price = 0

    return price


@app.route('/getMenuForStoreID', methods=['GET'])
def findNearbyStore():
    zip_code = request.args.get('zipCode')
    some_url = EXPRESS_SERVER + 'findStores/' + zip_code
    r = requests.get(some_url)
    j = r.json()

    if not j['success']:
        return bad_request('general error')

    the_store = False
    # find nearest open store that delivers
    for store in j['result']['Stores']:
        is_open = store['IsOpen']
        is_delivery_store = store['IsDeliveryStore']
        if is_open and is_delivery_store:
            the_store = store
            break
    # delete these after testing
    # if not the_store:
    #  return bad_request('no nearby stores exist, or none are open')
    the_store = j['result']['Stores'][0]

    # gather info about the store
    response = {}
    response['store_id'] = the_store['StoreID']
    response['phone'] = the_store['Phone']
    response['address'] = the_store['AddressDescription']
    response['delivery_times'] = the_store[
        'ServiceHoursDescription']['Delivery']

    # get menu and send back to client
    menu_url = EXPRESS_SERVER + 'getMenu/' + response['store_id']
    menu = json.loads(requests.get(menu_url).text)
    response['menu'] = menu['result']
    return json.dumps(response)


# Orders the pizza. Should pass the user though /validate first but this
# will run a validation check as well
@app.route('/order', methods=['POST'])
@payment.required(get_price) # get_price function call. If order is invalid, the user is not charged.
def order():
    if hasattr(request, 'error_validate'):
        return bad_request('There is a problem with your order details.')

    r = json.loads(requests.post(url=EXPRESS_SERVER + 'order',
                      json=json.loads(request.get_data(as_text=True))).text)

    response_status = r['result']['Status']

    if response_status == 0 or response_status == 1:
        order_id = r['result']['Order']['OrderID']
        response_text = 'Order placed! Your order ID is {0}'.format(order_id)
        response = {'status': 'success', 'text': response_text}
    else:
        response_text = 'Something in your order went wrong. Try again, friend.'
        response = {'status': 'error', 'text': response_text}

    return jsonify(response)


# Runs dominos validate function and should return price if the order
# details are valid, else return error
@app.route('/validate', methods=['POST'])
def validate():

    price_in_satoshi = get_price(request)

    if price_in_satoshi:

        products = json.loads(dominos_validation(request).text)['result']['Order']['Products']
        price_in_usd = json.loads(dominos_validation(request).text)['result']['Order']['Amounts']['Payment']

        product_list_for_reponse = ''
        for item in products:
            product_list_for_reponse += item['Name']
            product_list_for_reponse += ', '

        response_text = '{0}for {1} satoshi (${2}). Confirm? (yes/no)'.format(product_list_for_reponse, price_in_satoshi, price_in_usd)
        response = {'status': 'success', 'text': response_text}
    else:
        response_text = 'Something in your order went wrong. Try again, friend.'
        response = {'status': 'error', 'text': response_text}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
