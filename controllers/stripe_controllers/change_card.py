from stripe_keys import api_key
import stripe
from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id

def change_card(card_token):
    """
    change the current user's credit card information
    """

    google_id = users.get_current_user().user_id()
    user = get_user_by_google_id(google_id)
    customer = stripe.Customer.retrieve(user.stripeID)
    customer.card = card_token
    customer.save()
