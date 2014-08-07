from flask.views import MethodView
from flask import render_template

class PricingPage(MethodView):
    def get(self, pricing_type = None):
        if pricing_type == 'administrator':
            return render_template(
                'pricing_admin.html', 
                mathjax = False,
                )
        elif pricing_type == 'teacher':
            return render_template(
                'pricing_teacher.html', 
                mathjax = False
                )
        else:
            return render_template(
                'pricing.html', 
                mathjax = False
                )
