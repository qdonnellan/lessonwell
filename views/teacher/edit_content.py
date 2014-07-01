from flask.views import MethodView
from flask import render_template
from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id
from stripe_keys import pub_key

class EditContentPage(MethodView):
    """
    the request handler for the edit content page
    """
    
    def get(self):
        """
        handle the get request for the edit content page
        """
        user = get_user_by_google_id(users.get_current_user().user_id())
        return render_template(
            'edit.html',
            user = user,
            google_users_api = users,
            stripe_publish_key = pub_key,
            )