from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from flask import Flask, request, jsonify

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def handle_payment(request):
    bad_arguments = []
    if not request.args.get('address'):
        bad_arguments.append('address')
    if not request.args.get('pizza_type'):
        bad_arguments.append('pizza_type')
    if not request.args.get('delivery_time'):
        bad_arguments.append('delivery_time')

    if not len(bad_arguments):
        price = 1000  # satoshi
    else:
        setattr(request, 'bad_arguments', bad_arguments)
        price = 0

    return price


@app.route('/order')
@payment.required(handle_payment)
def myendpoint():
    bad_arguments = getattr(request, 'bad_arguments')
    if hasattr(request, 'bad_arguments'):
        return bad_request('You entered a bad argument(s): {}'.format(', '.join(bad_arguments)))

    return 'pizza time!'

# Set up and run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
