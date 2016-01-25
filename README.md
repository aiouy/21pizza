# 21pizza -- order pizza from your bitcoin computer

## Requirements

* [21 bitcoin computer](https://21.co)

## Instructions

`client.py` acts as the client for a hungry individual who wants to order a pizza. It sends requests to `server.py`, which is a bitcoin computer somewhere in the ether that is really good at ordering pizza.

`server.py` listens to `client.py`'s demands and sends requests to `order.js`.

`order.js` listens to `server.py` and calls dominos' APIs to fulfill the order.

* `npm install`
* Open up three command line terminals.
* Run `node order.js` on the first one. This one starts the dominos API server.
* Run `python3 server.py` on the second one. Now your 21 is listening for someone's pizza order.
* Run `python3 client.py` on the third. Run through the prompts and make sure you have enough bitcoin to pay for the pizza!
* Feast

## Todos

### client.py

- [X] Prompt user for zip code
- [X] Using zip code display menu to nearest store `[server.py: /getMenuForStoreID]`
- [X] Prompt user for menu item code(s)
- [X] Confirm menu & store location
- [X] Prompt user for full address
- [X] Build order and send request to server.py for verification `[server.py: /validate]`
- [X] Server.py returns price if order is valid and prompts confirmation of payment in usd & satoshi. If order is not valid, throw error
- [ ] Complete order `[server.py: /order]`
- [ ] Return order confirmation

### server.py


- [X] Receive zip code from client.py, call order.js `[/findStores/:zipCode]` to find nearest store
- [X] Get store menu by calling order.js `[/getMenu/:storeId]` and return store location & menu to client.py
- [X] Validate passing order to order.js `[/validateAndPrice]` using function `get_price`
- [X] If order is valid, find bitpay bbb usd/btc rate and return price to client.py
- [ ] Receive confirmed order, run though `get_price` again and set `[/order]` endpoint `@payment.required(get_price)` to price in satoshi


### order.js

- [X] Run `dominos` npm package to connect to dominos' ordering API.
- [ ] Store credit/debit card to order pizza
- [ ] Create a bitpay/coinbase invoice to pay credit card invoice
- [ ] Connect to Shake API to issue a one-time use card for every transaction

## Contributors

* @Melvillian
* @roybrey
