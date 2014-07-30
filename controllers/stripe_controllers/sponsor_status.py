import stripe
from stripe_keys import api_key

def sponsored(teacher):
    """
    return True if teacher is currently sponsored, False otherwise
    """
    stripe.api_key = api_key

    stripeID = teacher.stripeID
    customer = stripe.Customer.retrieve(stripeID)
    subscription = customer.subscriptions.data[0]
    
    status = False

    if subscription.discount and subscription.discount.coupon:
        if subscription.discount.coupon.id == 'sponsored':
            status = True

    return status

