#!/usr/bin/env python3
# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

import json

# Configure your Bitcoin wallet.
username = Config().username
wallet = Wallet()
requests = BitTransferRequests(wallet, username)

# server address
server_url = 'http://localhost:5000/'


def pizza():

    order_object = {


        ###################
        #   Who's hungry  #
        ###################

        'customer': {
            'firstName': 'Barack',
            'lastName': 'Obama',
            'address': '900 Clark Ave, St. Louis, MO, 63102', # all fields required here. Note the commas
            'phone': '1-212-222-2222',
            'email': 'barack@obama.com'
        },


        ###################
        #       Menu      #
        ###################
        #
        # Small (10") Gluten Free Crust Pizza, code: P10IGFZA
        # Medium (14") Hand Tossed Pizza, code: 14SCREEN
        # Large (16") Hand Tossed Pizza, code: 16SCREEN
        # X-Large (16") Hand Tossed Honolulu Hawaiian Pizza, code: P16IREUH
        # X-Large (16") Hand Tossed Philly Cheese Steak, code: P16IREPH
        #

        'item': {
            'code': "14SCREEN",
            'quantity': 1
        },


        ###################
        #     Store ID    #
        ###################
        #
        #
        'storeID': 1234 # int

    }

    ########### DO NOT EDIT BELOW ###########


    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    answer = requests.post(url=order_url, data=json.dumps(order_object), headers=headers)

    return answer.text


# start
if __name__ == '__main__':
    pizza()
