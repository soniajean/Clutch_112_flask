from flask import Blueprint, jsonify, request
import stripe
import os
import json
from ..models import Product


payments = Blueprint('payments', __name__, url_prefix='/pay')

stripe.api_key = os.environ.get('STRIPE_API_KEY')

def check_total(cart):
    """
    loop through the cart
    grab the price from OUR side
    calculate the total
    """
    total = 0 
    # print('Check total begin', cart)

    for product in cart['products']:
        p = Product.query.get(cart['products'][product]['data']['id']).price
        print(p)
        total += p*cart['products'][product]['quantity']
    # print(f'check_total return amount ->{total}')
    return total*100


def getCustomer(user):
    """
    Kinda like with Pokemon:  we want to check and see if we have the user first.
    if we do, cool grab that user.
    else --> create that user

    aka check stripe but make it talk with firebase auth
    """
    # we've seen the flask-sqlAlchemy version:
    #  Customer.query.get(id)
    try:
        customer = stripe.Customer.retrieve(user['uid'])
    except:
        customer = stripe.Customer.create(id=user['uid'], name=user['displayName'])
    # print(customer)
    return customer


@payments.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # print(data)
        intent = stripe.PaymentIntent.create(
            amount=check_total(data['cart']),
            customer = getCustomer(data['user']),      
            currency='usd',
            payment_method_types=['card']
        )
        return jsonify({'clientSecret': intent['client_secret']}), 200
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 403
    
