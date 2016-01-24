import json
import requests
import sys
import os

# server address
server_url = 'http://localhost:5000/'

# mock order data
order = {
    "customer": {
        "firstName": os.getenv('FIRST_NAME', 'Joey'),
        "lastName": os.getenv('LAST_NAME', 'Pizzaro'),
        "address": {
            "Street": os.getenv('STREET', '3375 Oak Lane Unit 22'),
            "City": os.getenv('CITY', 'Springfield'),
            "Region": os.getenv('REGION', 'CA'),
            "PostalCode": os.getenv('POSTAL_CODE', '95370')
        },
        "phone": os.getenv('PHONE', '8001112222'),
        "email": os.getenv('EMAIL', 'nobody@gmail.com')
    },

    # note: defaults might fail because these items are not on the menu
    # of the store whose ID is STORE_ID
    "items": [os.getenv('ITEM1', 'B8PCSCB'), os.getenv('ITEM2', '8TWISTY')],

    "storeID": os.getenv('STORE_ID', '7931'),

    # fake credit card account, should fail
    "cardNumber": os.getenv('PIZZAPI_CARD_NUMBER', '4242424242424242'),
    "cardExp": os.getenv('PIZZAPI_CARD_EXPIRATION', '0115'),
    "cardCCV": os.getenv('PIZZAPI_CARD_CVV', '007'),
    "cardZip": os.getenv('PIZZAPI_CARD_ZIP', '90210')
}


# get menu
# find_stores_url = server_url + 'getMenuForStoreID?zipCode=' + order['customer']['address']['PostalCode']
# r = requests.get(url=find_stores_url).json()

# validate the user's order and return the price in USD
resp = json.loads(requests.post(server_url + 'validate', json=order).text)

# check if order details are valid
if resp['status'] == 'success':
    # ask user for confirmation
    confirm = input(resp['text']+'\n')
    if confirm == 'yes':
        print('Placing order...')
        order = json.loads(requests.post(server_url + 'order', json=order).text)
        print(order['text'])
        # if error, exit
        if order['status'] == 'error':
            sys.exit(1)

else:
    print(resp['text'])
    sys.exit(1)
