from flask.views import MethodView
from flask import render_template
from google.appengine.api import users
from controllers.fetch_user import get_active_user

class LinkPage(MethodView):
    """
    the request handler for the page that prompts users to 
    link their google account
    """
    
    def get(self):
        """
        render the link page
        """
        return render_template(
            'link.html', 
            google_users_api = users, 
            active_user = get_active_user(),
            )