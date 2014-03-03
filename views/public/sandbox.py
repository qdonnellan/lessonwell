from views.main_view_handler import ViewHandler

class Sandbox(ViewHandler):
    '''
    the request handler for the sandbox page
    '''
    def get(self):
        '''
        handle the get request for the sandbox page
        '''
        self.render('sandbox.html')