#!/usr/bin/env python3
# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

import json
import sys
import random

# Configure your Bitcoin wallet.
username = Config().username
wallet = Wallet()
requests = BitTransferRequests(wallet, username)

# farewells to use when user wishes to end client flow
bitcoin_pizza_goodbyes = ["Well, we hope you have a nice day, even without that tasty Bitcoin pizza!",
                   "To the moon!!! ┗(°0°)┛",
                   "Bitcoin for pizza? Sounded like a crazy idea anyway!",
                   "Keep calm and HODL!",
]

# server address
server_url = "http://localhost:5000/"


def pizza():

    print("You are only a few steps away from buying Domino's pizza, 100% funded by Bitcoin!\n")
    print("We'll need you to:\n  * Pick a nearby store\n  * Select your meal from the Domino's menu\n  * Enter your delivery information")

    # acquire zip code and then get menu for domino"s near zip code
    zip_code = input("\nWhat is the zip code where you want your pizza delivered to: ")
    find_stores_url = server_url + "getMenuForStoreID?zipCode=" + str(zip_code)
    r = requests.get(url=find_stores_url).json()

    # check if user is ok with nearest store
    print("\nAddress:        " + r["address"])
    print("Phone:          " + r["phone"])
    print("Delivery Times: " + r["delivery_times"] + "\n")
    ok = input("The above Domino's store will prepare and deliver your meal. Type 'ok' if this store works for you: ")
    if ok != "ok":
        print("\n" + random.choice(bitcoin_pizza_goodbyes))
        sys.exit(1)

    print("\n\n")
    print("######################################")
    print("#                Menu                #")
    print("######################################")
    counter = 0
    for menuItem in r["menu"]:
        print("(" + str(counter) + ") " + str(list(menuItem.keys())[0]))
        counter = counter + 1
    print("######################################")
    print("#                Menu                #")
    print("######################################")
    print("\n")


    # get desired menu items from user
    orderItems = input("\nPlease give a comma separated list of the indices of the items you'd like to order from the menu above: ")
    orderItems = orderItems.split(",")
    chosenItems = []
    for index in orderItems:
        chosenItems.append(r["menu"][int(index)])

    # make sure user typed the items they wanted
    print("\n")
    for i in chosenItems:
        print(i)
    ok = input("Are the above choices correct? type 'ok' if you want to order these items: ")
    if ok != "ok":
        print("\n" + random.choice(bitcoin_pizza_goodbyes))
        sys.exit(1)

    # get info necessary to create order
    print("\nPlease enter the following information necessary to create your order")
    parameters = {}
    customer = {}
    customer["firstName"] = input("First Name: ")
    customer["lastName"] = input("Last Name: ")
    customer["phone"] = input("Phone Number: ")
    customer["email"] = input("Email: ")
    address = {}
    address["street"] = input("Street Address: ")
    address["city"] = input("City: ")
    address["Region"] = input("State: ")
    address["PostalCode"] = input("Zip Code: ")
    customer["address"] = address
    parameters["customer"] = customer
    parameters["items"] = [list(x.values())[0] for x in chosenItems]
    parameters["storeID"] = r["store_id"]

    # validate the user"s order and return the price in USD
    resp = json.loads(requests.post(server_url + 'validate', json=parameters).text)

    # check if order details are valid
    if resp['status'] == 'success':
        # ask user for confirmation
        confirm = input(resp['text']+'\n')
        if confirm == 'yes':
            print('Placing order...')
            order = json.loads(requests.post(server_url + 'order', json=parameters).text)
            print(order['text'])
            # if error, exit
            if order['status'] == 'error':
                sys.exit(1)

    else:
        print(resp['text'])
        sys.exit(1)

# start
if __name__ == "__main__":
    pizza()
