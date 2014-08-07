from flask.views import MethodView
from flask import render_template

class GooglePage(MethodView):
    """
    render a template which instructs on how we use Google Authentication
    """
    
    def get(self):
        """
        render the google page
        """
        return render_template('google.html')