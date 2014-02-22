from views.main_view_handler import ViewHandler
from decorators.auth import google_user_required
from stripe_keys import api_key
import datetime
import stripe

class SignUpPage(ViewHandler):
    '''
    the request handler for the sign_up page
    '''
    
    @google_user_required
    def get(self):
        '''
        render the sign_up page
        '''
        stripe_plan = stripe.Plan.retrieve('standard', api_key = api_key)
        trialEnd = datetime.datetime.now() + datetime.timedelta(days=stripe_plan.trial_period_days)
        trialEnd = trialEnd.strftime("%A, %B %d").replace(' 0', ' ')
        planAmount = stripe_plan.amount/100
        planAmount = "%1.2f"  % planAmount
        self.render('sign_up.html',
            trialEnd = trialEnd,
            planAmount = planAmount)