from flask.views import MethodView
from flask import render_template
from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id

class SuccessPage(MethodView):
    """
    handle the success page after a successful sign-up
    """
    
    def get(self):
        """
        render the success page
        """
        user = get_user_by_google_id(users.get_current_user().user_id())
        if user:
            return render_template(
                'success.html', 
                google_users_api = users,
                user = user,
                )