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

def get_price(request):
    return int(request.args['price'])

@app.route('/order')
@payment.required(get_price)
def order():
    return 'Awesome'

@app.route('/validate')
@payment.required(100)
def validate
    return 'nothing'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
