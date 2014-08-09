from flask.views import MethodView
from flask import render_template
from controllers.fetch_user import get_active_user
from google.appengine.api import users

class AboutPage(MethodView):
    def get(self):
        return render_template(
            'about.html', 
            active_user = get_active_user(),
            google_users_api = users,
            )

class PrivacyPage(MethodView):
    def get(self):
        return render_template(
            'privacy.html', 
            active_user = get_active_user(),
            google_users_api = users,
            )

class TermsPage(MethodView):
    def get(self):
        return render_template(
            'terms.html', 
            active_user = get_active_user(),
            google_users_api = users,
            )