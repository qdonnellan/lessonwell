import stripe
from stripe_keys import api_key

def new_customer(stripeToken, email, user=None):
    '''
    create a new customer and subscribe them to the standard plan

    return the customerID if successful, otherwise return False
    '''
    if user:
        stripe.api_key = api_key
        customer = stripe.Customer.create(
          card=stripeToken,
          plan="standard",
          email=email
        )
        user.stripeID = customer.id
        user.put()
        return True
    else:
        return False

