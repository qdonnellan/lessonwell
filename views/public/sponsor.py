from flask.views import MethodView
from controllers.fetch_user import get_user_by_username
from flask import render_template, request
from google.appengine.api import users
from stripe_keys import pub_key
from controllers.stripe_controllers.new_sponsor import new_sponsor
from controllers.stripe_controllers.sponsor_status import sponsored

class SponsorPage(MethodView):
    """
    the request handler for the profile page
    """
    
    def get(self, username):
        """
        get request displays the teacher's sponsor page
        """
        teacher = get_user_by_username(username)
        if sponsored(teacher):
            return render_template(
                'already_sponsored.html', 
                teacher = teacher
            )
        else:
            return render_template(
                'sponsor.html', 
                teacher = teacher,
                stripe_publish_key = pub_key,
            )

    def post(self, username):
        """
        handle the sponsor payment
        """
        stripeToken = request.form['stripeToken']
        teacher = get_user_by_username(username) 
        try:
            new_sponsor(stripeToken, teacher)
        except Exception as e:
            return render_template(
                'sponsor.html', 
                teacher = teacher,
                stripe_publish_key = pub_key,
                error = True,
                error_msg = str(e),
                )
        else:
            return render_template(
                'sponsor_success.html', 
                teacher = teacher
                )
