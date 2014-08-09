from flask.views import MethodView
from flask import render_template

class LandingPage1(MethodView):
    def get(self):
        return render_template(
            'stop_wasting_time.html',
            mathjax = False
            )
