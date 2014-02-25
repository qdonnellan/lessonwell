import stripe

def new_customer(stripeToken, email, user=None):
    '''
    create a new customer and subscribe them to the standard plan

    return the customerID if successful, otherwise return False
    '''
    if user:
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

