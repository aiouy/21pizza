import json
import urllib.request as request

price_in_usd = 34.55
get_bitpay_btc_usd_rate = request.urlopen(url="https://bitpay.com/api/rates/usd").read().decode("utf-8")
data = json.loads(get_bitpay_btc_usd_rate)["rate"]

print(data)
# price = price_in_usd * 10^8 / get_bitpay_btc_usd_rate.rate
# print(price)
