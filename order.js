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


app.post('/validateAndPrice', function(req, res) {

  var order = createOrder(req.body);

  order.validate(
    function(validateResult) {
      // console.log("Validate! " + JSON.stringify(validateResult, null, 4));
      order.price(
        function(priceResult) {
          // console.log("Price! " + JSON.stringify(priceResult, null, 4));
          console.log(JSON.stringify(order, null, 4));
          res.send(JSON.stringify(priceResult, null, 4));
        }
      );

    }
  );

});

app.post('/order', function(req, res) {

  console.log('Ordering...');

  var order = createOrder(req.body);

  var cardNumber = process.env.PIZZAPI_CARD_NUMBER || '2222333344445555';
  var expiration = process.env.PIZZAPI_CARD_EXPIRATION || '0115';
  var securityCode = process.env.PIZZAPI_CARD_SEC_CODE || '007';
  var postalCode = '90210'; // Billing Zipcode

  var cardInfo = new order.PaymentObject();
  cardInfo.Amount = order.Amounts.Customer;
  cardInfo.Number = cardNumber;
  cardInfo.CardType = order.validateCC(cardNumber);
  cardInfo.Expiration = expiration; //  01/15 just the numbers "01/15".replace(/\D/g,'');
  cardInfo.SecurityCode = securityCode;
  cardInfo.PostalCode = postalCode; // Billing Zipcode

  order.Payments.push(cardInfo);

  order.place(
    function(result) {
      console.log("Order placed!");
      res.send(JSON.stringify(result, null, 4));
    }
  );

});


function createOrder(requestBody) {
  console.log('Creating Order...');

  var customer = new pizzapi.Customer(requestBody.customer);

  var order = new pizzapi.Order({
    customer: customer,

    //optional set the store ID right away
    storeID: requestBody.storeID,

    deliveryMethod: 'Delivery' //Carryout
  });

  var item = new pizzapi.Item(requestBody.item);

  order.addItem(item);

  order.Phone = requestBody.customer.phone;

  return order;

}

app.listen(3000, function() {
  console.log('Listening on port 3000!');
});
