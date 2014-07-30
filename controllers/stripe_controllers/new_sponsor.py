import stripe
from stripe_keys import api_key

def new_sponsor(token, teacher):
    """
    create a new Sponsorship for teacher paid for by the token
    """
    stripe.api_key = api_key

    # charge the card
    charge = stripe.Charge.create(
        amount=8900, # amount in cents
        currency="usd",
        card=token,
        description="1 Year Sponsorship of %s" % teacher.formalName
    )

    # add the sponsorship
    stripeID = teacher.stripeID
    customer = stripe.Customer.retrieve(stripeID)
    subscription = customer.subscriptions.data[0]
    subscription.coupon = 'sponsored'
    subscription.save()