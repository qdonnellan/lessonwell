from flask.views import MethodView
from flask import render_template

class FrontPage(MethodView):
    def get(self):
        return render_template('front.html', homeActive='active')