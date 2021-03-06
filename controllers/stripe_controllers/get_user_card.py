from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id
from stripe_keys import api_key
import stripe

def get_user_card():
    """
    return card information for the current user
    """

    stripe.api_key = api_key

    google_user = users.get_current_user()
    googleID = google_user.user_id()
    local_user = get_user_by_google_id(googleID)

    stripeID = local_user.stripeID
    customer = stripe.Customer.retrieve(stripeID)
    # return the first card from the customer's card list

    data = {}
    data['card'] = customer.cards.data[0]
    
    return customer.cards.data[0]




