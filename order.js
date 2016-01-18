var express = require('express');
var bodyParser = require('body-parser');
var pizzapi = require('pizzapi');

var app = express();

app.use(bodyParser.json());

app.get('/findStores/:zipCode', function(req, res) {

  var zipCode = req.params.zipCode;

  pizzapi.Util.findNearbyStores(
      zipCode,
      'Delivery',
      function(storeData){
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

  console.log(JSON.stringify(req.body, null, 4));
  var order = createOrder(req.body);

  order.validate(
    function(validateResult) {
      console.log("Validate! " + JSON.stringify(validateResult, null, 4));
      order.price(
        function(priceResult) {
          console.log("Price! " + JSON.stringify(priceResult, null, 4));
          res.send(JSON.stringify(validateResult, null, 4));
        }
      );

    }
  );

});

app.post('/order', function(req, res) {

  console.log('Ordering...');

  res.send("Order sent");

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

  return order;

}

app.listen(3000, function() {
  console.log('Listening on port 3000!');
});
