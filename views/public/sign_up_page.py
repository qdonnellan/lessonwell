from views.main_view_handler import ViewHandler
from decorators.auth import link_if_no_google_user, abort_if_no_google_user
from controllers.validation import validate_username
from controllers.modify_user import new_user
from controllers.stripe_controllers.new_customer import new_customer
from google.appengine.api import users
import datetime

class SignUpPage(ViewHandler):
    '''
    the request handler for the sign_up page
    '''
    
    @link_if_no_google_user
    def get(self):
        '''
        render the sign_up page
        '''
        trialEnd = datetime.datetime.now() + datetime.timedelta(days=30)
        trialEnd = trialEnd.strftime("%A, %B %d").replace(' 0', ' ')
        planAmount = "10.00"
        self.render('sign_up.html',
            trialEnd = trialEnd,
            planAmount = planAmount)

    @abort_if_no_google_user
    def post(self):
        '''
        handle a post request, which may or may not contain errors
        '''
        username = self.request.get('username')
        stripeToken = self.request.get('stripeToken')
        formalName = self.request.get('formalName')
        email = users.get_current_user().email()
        try: 
            validate_username(username)
            if not stripeToken or stripeToken == '': 
                raise NameError('Invalid Payment Information')
            user = new_user(
                username = username, 
                formalName = formalName, 
                email = email,
                googleID = users.get_current_user().user_id()
                )
            if not user:
                raise NameError('There was a problem creating your user account, please try again')
            new_customer(stripeToken, email, user)

        except Exception as e:
            self.write(str(e))
            self.redirect('/sign_up?error=%s' % e)
        else:
            self.redirect('/success')

