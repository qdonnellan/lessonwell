from flask.views import MethodView
from controllers.fetch_user import get_user_by_username, get_active_user
from flask import render_template
from google.appengine.api import users


class ProfilePage(MethodView):
    """
    the request handler for the profile page
    """
    
    def get(self, username):
        """
        get request displays the teacher's profile page
        """
        teacher = get_user_by_username(username)
        return render_template(
            'profile.html', 
            teacher = teacher,
            active_user = get_active_user(),
            google_users_api = users,
            mathjax = True
            )