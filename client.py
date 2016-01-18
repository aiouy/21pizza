#!/usr/bin/env python3
# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

import json
import sys

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
            'firstName': 'Alex',
            'lastName': 'Bitcoins',
            'address': {
                'street': '532 Tyrella Ave #39',
                'city': 'Mountain View',
                'Region': 'CA', # two letter state code (eg: DC, CA)
                'PostalCode': '94043' # 5-digit zip code
            },
            'phone': '8023564779',
            'email': 'habs7707@gmail.com'
        },


        ###################
        #       Menu      #
        ###################


        'item': {
            'code': "W40PHOTW",
            'quantity': 1
        },


        ###################
        #     Store ID    #
        ###################
        #
        #
        'storeID': '7931'  # string

    }

    ########### DO NOT EDIT BELOW ###########

    task = input("Tasks (enter 1, 2, 3):\n1. Find store ID\n2. Validate inputs and get price (this should always be done first)\n3. Order\n")
    if int(task) == 1:
        print('Awesome!')
    elif int(task) == 2:
        order_url = server_url + 'validate'
    elif int(task) == 3:
        order_url = server_url + 'order'
    else:
        print('Please enter either 1, 2, or 3')
        sys.exit()

    answer=requests.post(url=order_url, data=order_object)

    print(answer.text)


# start
if __name__ == '__main__':
    pizza()
