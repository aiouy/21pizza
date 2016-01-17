#!/usr/bin/env python3
# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# Configure your Bitcoin wallet.
username = Config().username
wallet = Wallet()
requests = BitTransferRequests(wallet, username)

def get_matches():
    url = 'http://' + SERVER_IP_ADDRESS + ':5000/nhlMatches'
    r = requests.get(url=url)

    print(r.text)



# start
if __name__ == '__main__':
    get_matches()
