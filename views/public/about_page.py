from views.main_view_handler import ViewHandler

class AboutPage(ViewHandler):
    '''
    the request handler for the public about pages
    '''
    
    def get(self):
        '''
        handle the get request for the TOS, Privacy, and About document pages
        '''
        self.render(
            'about.html', 
            doc = self.request.get('doc'), 
            left_panel = True
            )