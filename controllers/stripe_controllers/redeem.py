import stripe
from stripe_keys import api_key
import logging

def redeem_code(teacher, coupon_code):
    """
    redeem coupon code and apply coupon to teacher if possible
    """
    stripe.api_key = api_key
    stripeID = teacher.stripeID
    customer = stripe.Customer.retrieve(stripeID)
    customer.coupon = coupon_code
    customer.save()

def verify_code(coupon_code):
    """
    verfiy the coupon_code and return True. 

    If invalid, return False
    """
    stripe.api_key = api_key
    try:
        coupon = stripe.Coupon.retrieve(coupon_code)
    except Exception as e:
        logging.info(e)
        return False
    else:
        return True
        

