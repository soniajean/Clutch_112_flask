from flask import Blueprint, jsonify, request
import stripe
import os
import json


payments = Blueprint('payments', __name__, url_prefix='/pay')

stripe.api_key = os.environ.get('STRIPE_API_KEY')

def check_total(cart):
    """
    checks the cart and totals the items to determine if correct
    --> return True
    """
    return True

@payments.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        print(data)
        intent = stripe.PaymentIntent.create(
            amount=100,
            # customer = user,          TO-DO
            currency='usd',
            payment_method_types=['card']
        )
        return jsonify({'clientSecret': intent['client_secret']}), 200
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 403
    
