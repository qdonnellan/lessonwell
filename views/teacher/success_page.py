from views.main_view_handler import ViewHandler
from decorators.auth import local_user_required

class SuccessPage(ViewHandler):
    '''
    the request handler for the sign-up success page
    '''
    
    @local_user_required
    def get(self):
        '''
        handle the get request for the success page
        '''
        self.render('sign_up_success.html')