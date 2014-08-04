from flask.views import MethodView
from flask import render_template, request, redirect, url_for
from stripe_keys import pub_key
from decorators.auth import link_if_no_google_user, abort_if_no_google_user
from controllers.validation import validate_username
from controllers.modify_user import new_user
from controllers.stripe_controllers.new_customer import new_customer
from controllers.stripe_controllers.redeem import verify_code
from google.appengine.api import users
import datetime

class SignUpPage(MethodView):
    """
    the request handler for the sign up page
    """

    def get(self):
        """
        handle the get request for the signup page
        """

        if not users.get_current_user():
            return redirect('/link')
        else:
            trialEnd = datetime.datetime.now() + datetime.timedelta(days=30)
            trialEnd = trialEnd.strftime("%A, %B %d").replace(' 0', ' ')
            planAmount = "10.00"

            return render_template(
                'sign_up.html', 
                trialEnd = trialEnd,
                planAmount = planAmount,
                google_users_api = users,
                stripe_publish_key = pub_key
                )


