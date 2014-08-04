import stripe
from stripe_keys import api_key
from controllers.stripe_controllers.redeem import redeem_code

def new_customer(email, user, coupon_code=None):
    """
    create a new customer and subscribe them to the standard plan

    return the customerID if successful, otherwise return False
    """
    if user:
        stripe.api_key = api_key

        customer = stripe.Customer.create(
          plan="standard",
          email=email
        )
        user.stripeID = customer.id
        user.put()

        if coupon_code and coupon_code != '':
            redeem_code(
                teacher = user,
                coupon_code = coupon_code,
            )
        return True
    else:
        return False

