// Express server code adapted from
// https://github.com/RIAEvangelist/node-dominos-pizza-api
var express = require('express');
var bodyParser = require('body-parser');
var pizzapi = require('dominos');

var app = express();

app.use(bodyParser.json());

app.get('/findStores/:zipCode', function(req, res) {

  var zipCode = req.params.zipCode;

  pizzapi.Util.findNearbyStores(
    zipCode,
    'Delivery',
    function(storeData) {
      var prettyStoreData = JSON.stringify(storeData, null, 4);
      res.send(prettyStoreData);
    }
  );

});

app.get('/getMenu/:storeId', function(req, res) {
  console.log('getting store menu...');
  storeId = parseInt(req.params.storeId);
  var myStore = new pizzapi.Store({
    ID: storeId
  });

  myStore.getFriendlyNames(
    function(storeData) {
      var prettyStoreData = JSON.stringify(storeData, null, 4);
      // console.log(prettyStoreData);
      res.send(prettyStoreData);
    }
  );

});

// validate the order is well-formed and send back
// the price of the order
app.post('/validateAndPrice', function(req, res) {
  var order = createOrder(req.body, false);

  order.validate(
    function(validateResult) {
      console.log("Validate! " + JSON.stringify(validateResult, null, 4));
      order.price(
        function(priceResult) {
          console.log("Price! " + JSON.stringify(priceResult, null, 4));
          res.send(JSON.stringify(priceResult, null, 4));
        }
      );

    }
  );

});

// Hit Domino's servers with a order
app.post('/order', function(req, res) {

  console.log('Ordering...');

  var order = createOrder(req.body, true);

  order.place(
    function(result) {
      var prettyResult = JSON.stringify(result, null, 4);
      console.log("Order placed!");
      console.log(prettyResult);
      res.send(prettyResult);
    }
  );

});

// Create a ready-to-send order based on
// customer menu choices, personal data,
// and billing data
function createOrder(requestBody, realOrder) {
  console.log('Creating Order...');

  var customer = new pizzapi.Customer(requestBody.customer);

  var order = new pizzapi.Order({
    customer: customer,

    //optional set the store ID right away
    storeID: requestBody.storeID,

    deliveryMethod: 'Delivery' //Carryout
  });

  var foodItems = requestBody.items;
  foodItems.forEach(function(code) {
    var item = {
      code: code,
      options: [],
      quantity: 1
    };
    order.addItem(new pizzapi.Item(item));
  });

  if (realOrder) {
    var cardNumber = requestBody.cardNumber;
    var expiration = requestBody.cardExp;
    var securityCode = requestBody.cardCCV;
    var postalCode = requestBody.cardZip;

    var cardInfo = new order.PaymentObject();
    cardInfo.Amount = order.Amounts.Customer;
    cardInfo.Number = cardNumber;
    cardInfo.CardType = order.validateCC(cardNumber);
    cardInfo.Expiration = expiration; //  01/15 just the numbers "01/15".replace(/\D/g,'');
    cardInfo.SecurityCode = securityCode;
    cardInfo.PostalCode = postalCode; // Billing Zipcode

    order.Payments.push(cardInfo);
  }

  return order;
}

app.listen(3000, function() {
  console.log('Listening on port 3000!');
});
