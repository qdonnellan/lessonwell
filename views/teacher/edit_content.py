from flask.views import MethodView
from flask import render_template, abort
from google.appengine.api import users
from controllers.fetch_user import get_active_user
from stripe_keys import pub_key

class EditContentPage(MethodView):
    """
    the request handler for the edit content page
    """
    
    def get(self):
        """
        handle the get request for the edit content page
        """
        if not users.get_current_user():
            abort(401)
        else:
            return render_template(
                'edit.html',
                active_user = get_active_user(),
                google_users_api = users,
                stripe_publish_key = pub_key,
                mathjax = True,
                )