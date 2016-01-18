import json
import urllib.request as request
import requests

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

    "item": {
        "code": "W40PHOTW",
        "options": [],
        "quantity": 1
    },

    "storeID": "7931"
}

r = requests.post('http://localhost:3000/validateAndPrice',
                 json=data_to_send)
response_data = json.loads(r.text)["result"]["Status"]
print(response_data)

# if response_data.result.Status == 1 or response_data.result.Status == 0:
#     price_in_usd = r.result.Order.Amounts.Payment
#
#     get_bitpay_btc_usd_rate = request.urlopen(
#         url="https://bitpay.com/api/rates/usd").read().decode("utf-8")
#     usd_per_btc = json.loads(get_bitpay_btc_usd_rate)["rate"]
#
#     price = price_in_usd * 10 ^ 8 / usd_per_btc
# else:
#     setattr(request, 'error_validate', 'error_validate')
#     price = 0
#
# return price
