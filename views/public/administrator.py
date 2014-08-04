from flask.views import MethodView
from flask import render_template, request
from google.appengine.api import users
from stripe_keys import pub_key
from controllers.stripe_controllers.new_sponsor import new_multi_sponsor


class AdministratorPage(MethodView):
    """
    the request handler adminstrator purchasing page
    """
    
    def get(self):
        """
        get request displays the purchasing page
        """
        return render_template(
            'administrator.html', 
            stripe_pub_key = pub_key,
            mathjax = False
        )

    def post(self):
        """
        post request completes the purchase of a multi-subscrition order
        """
        try:
            token = request.form['stripeToken']
            number_of_subscriptions = request.form['quantity']
            email= request.form['email']
            new_multi_sponsor(
                token = token,
                number_of_subscriptions = number_of_subscriptions,
                email = email,
            )
        except Exception as e:
            return render_template(
                'administrator.html',
                stripe_pub_key = pub_key,
                mathjax = False,
                error = str(e)
                )
        else:

            return render_template(
                'multi_sponsor_success.html',
                mathjax = False
                )






