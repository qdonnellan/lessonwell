import stripe
from stripe_keys import api_key
from controllers.sponsor_email import send_multi_subscription_confirmation

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
    customer.coupon = 'sponsored'
    customer.save()

def new_multi_sponsor(token, number_of_subscriptions, email):
    """
    create a multi-use coupon and send confirmation email with instructions
    """

    stripe.api_key = api_key

    # the pricing model
    pricing = {
        '5' : 42000, 
        '10' : 72000, 
        '20' : 96000
    }

    # charge the sponsor's credit card
    charge = stripe.Charge.create(
        amount=pricing[number_of_subscriptions],
        currency="usd",
        card=token,
        description="Purchase of %s subscriptions" % number_of_subscriptions
    )

    # create the coupon
    coupon = stripe.Coupon.create(
        percent_off = 100,
        duration = 'repeating',
        duration_in_months = 12,
        max_redemptions = int(number_of_subscriptions),
        metadata = {
            'sponsor': email,
            'description': 'multi-use',
            }
    )

    send_multi_subscription_confirmation(
        email = email, 
        quantity = number_of_subscriptions, 
        coupon_code = coupon.id
    )




