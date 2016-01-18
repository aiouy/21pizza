var pizzapi = require('pizzapi');

// Setup your Default Store
// 6371 = Lafayette, CO 80026
// Run `node findStore.js` and enter Zip Code
var myStore = new pizzapi.Store({
  ID: '7931'
});

// Setup your Address
var myAddress = new pizzapi.Address({
  Street: '532 Tyrella Ave #39',
  City: 'Mountain View',
  Region: 'CA',
  PostalCode: '94043'
});

// Setup your Customer
var myCustomer = new pizzapi.Customer({
  firstName: 'Alex',
  lastName: 'Bitcoins',
  address: myAddress,
  phone: '8023564779',
  email: 'habs7707@gmail.com'
});

var order = new pizzapi.Order({
  customer: myCustomer,
  storeID: myStore.ID
});

// Setup your Default Order
// 14SCREEN = Large (14") Hand Tossed Pizza Whole: Cheese
order.addItem(
  new pizzapi.Item({
    code: 'W40PHOTW',
    options: [],
    quantity: 1
  })
);

// Setup your Credit Card Info
// var cardNumber = '4100123422343234'; // Valid but fake credit card
// var cardInfo = new order.PaymentObject();
// cardInfo.Amount = order.Amounts.Customer;
// cardInfo.Number = cardNumber;
// cardInfo.CardType = order.validateCC(cardNumber);
// cardInfo.Expiration = '0115'; //  01/15 just the numbers "01/15".replace(/\D/g,'');
// cardInfo.SecurityCode = '777';
// cardInfo.PostalCode = '90210'; // Billing Zipcode
//
// order.Payments.push(cardInfo);


// var dash = dash_button(process.env.DASH_MAC_ADDRESS);
// dash.on("detected", function() {
  // console.log("Dash Button Found");
  //Validate, price, and place order!
  // order.validate(
  //   function(result) {
  //     console.log("Valitasdte: " + JSON.stringify(result, null, 4));
  //   }
  // );
  order.price(
    function(result) {
      console.log("Price: " + JSON.stringify(result, null, 4));
    }
  );
  // order.place(
  //   function(result) {
  //     console.log("Price is", result.result.Order.Amounts, "\nEstimated Wait Time", result.result.Order.EstimatedWaitMinutes, "minutes");
  //     console.log("Order placed!");
  //   }
  // );
// });
