from views.main_view_handler import ViewHandler

class LinkGoogleAccountPage(ViewHandler):
    '''
    the request handler for the page that prompts users to link their google account
    '''
    
    def get(self):
        '''
        render the link page
        '''
        self.render('link.html')