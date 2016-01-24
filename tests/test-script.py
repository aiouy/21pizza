import json
import requests

# server address
server_url = 'http://localhost:5000/'

data_to_send = {
    "customer": {
        "firstName": "Alex",
        "lastName": "Bitcoins",
        "address": {
            "Street": "532 Tyrella Ave #39",
            "City": "Mountain View",
            "Region": "CA",
            "PostalCode": "94043"
        },
        "phone": "8023564779",
        "email": "habs7707@gmail.com"
    },

    "items": ["W40PHOTW", "W40PPLNW", "W40PBNLW"],

    "storeID": "7931"
}

# get menu
# find_stores_url = server_url + 'getMenuForStoreID?zipCode=' + data_to_send['customer']['address']['PostalCode']
# r = requests.get(url=find_stores_url).json()

# validate the user's order and return the price in USD
resp = json.loads(requests.post(server_url + 'validate', json=data_to_send).text)

# check if order details are valid
if resp['status'] == 'success':
    # ask user for confirmation
    confirm = input(resp['text']+'\n')
    if confirm == 'yes':
        print('Placing order...')
        order = json.loads(requests.post(server_url + 'order', json=data_to_send).text)
        print(order['text'])
        # if error, exit
        if order['status'] == 'error':
            sys.exit(1)

else:
    print(resp['text'])
    sys.exit(1)
