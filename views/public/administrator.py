from flask.views import MethodView
from flask import render_template, request
from google.appengine.api import users
from stripe_keys import pub_key
from controllers.stripe_controllers.new_sponsor import new_sponsor
from controllers.stripe_controllers.sponsor_status import sponsored

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
