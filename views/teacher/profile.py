from flask.views import MethodView
from controllers.fetch_user import get_user_by_username
from flask import render_template
import logging

class ProfilePage(MethodView):
    """
    the request handler for the profile page
    """
    
    def get(self, username):
        """
        get request displays the teacher's profile page
        """
        teacher = get_user_by_username(username)
        return render_template('profile.html', teacher = teacher)