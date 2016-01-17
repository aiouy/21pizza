#!/usr/bin/env python3
# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# Configure your Bitcoin wallet.
username = Config().username
wallet = Wallet()
requests = BitTransferRequests(wallet, username)

# server address
server_url = 'http://localhost:5000/'

def pizza():

    #############
    #           #
    #   STEP 1  #
    #           #
    #############
    #
    # create customer object
    # customerObject = {
    # firstName: '',
    # lastName: '',
    # address: '',
    # email: ''
    # }

    order_url = server_url+'order?price={0}'
    answer = requests.get(url=order_url.format(int(500)))

    return answer.text



# start
if __name__ == '__main__':
    pizza()
