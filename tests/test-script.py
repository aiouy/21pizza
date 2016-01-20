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
find_stores_url = server_url + 'getMenuForStoreID?zipCode=' + data_to_send['customer']['address']['PostalCode']
r = requests.get(url=find_stores_url).json()

# validate the user's order and return the price in USD
resp = requests.post(server_url + 'validate', data=data_to_send)
print(resp.text)