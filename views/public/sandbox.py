from flask.views import MethodView
from flask import render_template
from controllers.fetch_user import get_active_user
from google.appengine.api import users

class SandboxPage(MethodView):
    def get(self):
        return render_template(
            'sandbox.html', 
            active_user = get_active_user(),
            google_users_api = users,
            )