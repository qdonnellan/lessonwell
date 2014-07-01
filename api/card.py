from flask.ext.restful import Resource, reqparse
from controllers.stripe_controllers.get_user_card import get_user_card
from controllers.stripe_controllers.change_card import change_card
from google.appengine.api import users


class CardAPI(Resource):
    """
    handle requests for a User's credit card information
    """
    def get(self):
        """
        return the user card if possible, else return an error
        """
        if not users.get_current_user():
            return {'error': 'you must be logged in to view this info'}, 401
        else:
            try:
                data = get_user_card()
            except Exception as e:
                data = {'error' : str(e)}
            return data