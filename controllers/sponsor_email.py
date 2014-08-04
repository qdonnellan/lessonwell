from google.appengine.api import mail

def send_multi_subscription_confirmation(email, quantity, coupon_code):
    """
    send confirmation email of multi-subscription purchase
    """
    sender_address = "sponsor@lessonwell.com"
    subject = "Lessonwell Purchase Confirmation"
    body = """

    Thank you for your purchase of %s subscriptions!

    Coupon code: %s

    Lessonwell Team


    """ % (quantity, coupon_code)

    mail.send_mail(sender_address, email, subject, body)


