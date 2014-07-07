from controllers.stripe_controllers.get_customer import get_customer
from flask.ext.restful import Resource, reqparse
from google.appengine.api import users

class CustomerAPI(Resource):
    """
    api handlers for customer objects
    """

    def get(self):
        current_user = users.get_current_user()
        if not current_user:
            return 401
        else:
            customer = get_customer()
            return customer